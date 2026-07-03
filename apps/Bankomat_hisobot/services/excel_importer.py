from pathlib import Path
from decimal import Decimal

from django.db import transaction
from openpyxl import load_workbook

from apps.Bankomat_hisobot.models import ATMType, Region, ATMModel, ATM, Branch, ATMStatistic, ATMStatus
from datetime import date

class ATMExcelImporter:
    """
    Excel importer

    - Faqat FULL sheetni o'qiydi
    - Merge qilingan kataklarni tiklaydi
    - Headerlarni tekshiradi
    - Rowlarni dict ko'rinishida qaytaradi
    """

    SHEET_NAME = "FULL"

    REQUIRED_HEADERS = [
        "№",
        "BXM",
        "Joylashgan joyi",
        "Bankomat turi",
        "Bankomat modeli",
        "Holati",
        "Seriya raqami",
        "Inventar raqami",
        "Yuridik manzili",
        "Merchant ID",
        "Terminal ID",
        "Ohirgi 3 oylik chiqim",
        "Ohirgi 3 oylik daromad",
    ]

    def __init__(self, file_path):

        self.file_path = Path(file_path)

        self.workbook = None

        self.sheet = None

        self.headers = {}

        self.previous_branch = None

        self.previous_region = None

        self.previous_address = None

        # ==========================
        # CACHE
        # ==========================

        self.region_cache = {}

        self.branch_cache = {}

        self.type_cache = {}

        self.model_cache = {}

        self.atm_cache = {}

        # ==========================
        # IMPORT REPORT
        # ==========================

        self.created = 0

        self.updated = 0

        self.errors = []

    def load_cache(self):

        """
        Database dagi barcha ma'lumotlarni RAM ga yuklaydi.
        """

        self.region_cache = {
            region.name.lower(): region
            for region in Region.objects.all()
        }

        self.type_cache = {
            item.name.lower(): item
            for item in ATMType.objects.all()
        }

        self.model_cache = {
            item.name.lower(): item
            for item in ATMModel.objects.all()
        }

        self.atm_cache = {}

        for atm in ATM.objects.all():

            if atm.serial_number:
                self.atm_cache[("serial", atm.serial_number)] = atm

            if atm.merchant_id:
                self.atm_cache[("merchant", atm.merchant_id)] = atm

            if atm.terminal_id:
                self.atm_cache[("terminal", atm.terminal_id)] = atm

        self.branch_cache = {}

        for branch in Branch.objects.select_related("region"):
            key = (
                branch.region.name.lower(),
                branch.name.lower()
            )

            self.branch_cache[key] = branch

    def get_region(self, name):

        if not name:
            raise ValueError("Region nomi bo'sh")

        key = name.strip().lower()

        if key in self.region_cache:
            return self.region_cache[key]

        region = Region.objects.create(
            name=name.strip()
        )

        self.region_cache[key] = region

        return region


    def get_branch(
            self,
            region,
            name,
            legal_address,
    ):
        """
        Branch ni cache yoki databasedan oladi.
        Agar bo'lmasa yaratadi.
        """

        if not name:
            raise ValueError("Branch nomi bo'sh.")

        key = (
            region.name.lower(),
            name.strip().lower(),
        )

        if key in self.branch_cache:
            return self.branch_cache[key]

        branch = Branch.objects.create(
            region=region,
            name=name.strip(),
            legal_address=legal_address.strip() if legal_address else "",
        )

        self.branch_cache[key] = branch

        return branch

    def get_atm_type(self, name):
        """
        ATM turini cache yoki databasedan oladi.
        """

        if not name:
            raise ValueError("ATM turi bo'sh.")

        key = name.strip().lower()

        if key in self.type_cache:
            return self.type_cache[key]

        atm_type = ATMType.objects.create(
            name=name.strip()
        )

        self.type_cache[key] = atm_type

        return atm_type

    def get_atm_model(self, name):
        """
        ATM modelini cache yoki databasedan oladi.
        """

        if not name:
            raise ValueError("ATM modeli bo'sh.")

        key = name.strip().lower()

        if key in self.model_cache:
            return self.model_cache[key]

        model = ATMModel.objects.create(
            name=name.strip()
        )

        self.model_cache[key] = model

        return model

    def get_or_create_atm(
            self,
            branch,
            atm_type,
            atm_model,
            row,
    ):
        """
        ATM ni yaratadi yoki yangilaydi.
        """

        serial_number = row["serial_number"]

        status = (
            ATMStatus.ACTIVE
            if row["status"].lower() == "soz"
            else ATMStatus.INACTIVE
        )

        # Cache dan tekshiramiz
        if serial_number in self.atm_cache:

            atm = self.atm_cache[serial_number]

            changed = False

            if atm.branch_id != branch.id:
                atm.branch = branch
                changed = True

            if atm.atm_type_id != atm_type.id:
                atm.atm_type = atm_type
                changed = True

            if atm.atm_model_id != atm_model.id:
                atm.atm_model = atm_model
                changed = True

            if atm.status != status:
                atm.status = status
                changed = True

            if atm.inventory_number != row["inventory_number"]:
                atm.inventory_number = row["inventory_number"]
                changed = True

            if atm.merchant_id != row["merchant_id"]:
                atm.merchant_id = row["merchant_id"]
                changed = True

            if atm.terminal_id != row["terminal_id"]:
                atm.terminal_id = row["terminal_id"]
                changed = True

            if changed:
                atm.save()

                self.updated += 1

            return atm

        atm = ATM.objects.create(

            branch=branch,

            atm_type=atm_type,

            atm_model=atm_model,

            status=status,

            serial_number=serial_number,

            inventory_number=row["inventory_number"],

            merchant_id=row["merchant_id"],

            terminal_id=row["terminal_id"],
        )

        self.atm_cache[serial_number] = atm

        self.created += 1

        return atm

    @transaction.atomic
    def import_data(self):

        self.load_cache()

        for row in self.read():
            region = self.get_region(
                row["region"]
            )

            branch = self.get_branch(
                region=region,
                name=row["branch"],
                legal_address=row["legal_address"],
            )

            atm_type = self.get_atm_type(
                row["atm_type"]
            )

            atm_model = self.get_atm_model(
                row["atm_model"]
            )

            atm = self.get_or_create_atm(
                branch=branch,
                atm_type=atm_type,
                atm_model=atm_model,
                row=row,
            )

            self.save_statistic(
                atm,
                row,
            )

        return {

            "created": self.created,

            "updated": self.updated,

            "errors": len(self.errors),

        }

    def save_statistic(
            self,
            atm,
            row,
    ):

        ATMStatistic.objects.update_or_create(

            atm=atm,

            period=date.today().replace(day=1),

            defaults={

                "expense": row["expense"],

                "income": row["income"],

            }

        )
    def load_workbook(self):

        if not self.file_path.exists():
            raise FileNotFoundError(self.file_path)

        self.workbook = load_workbook(
            filename=self.file_path,
            data_only=True
        )

        if self.SHEET_NAME not in self.workbook.sheetnames:
            raise Exception(
                f"{self.SHEET_NAME} sheet topilmadi."
            )

        self.sheet = self.workbook[self.SHEET_NAME]


    def load_headers(self):

        for cell in self.sheet[1]:

            if cell.value:

                self.headers[str(cell.value).strip()] = cell.column

        missing = []

        for header in self.REQUIRED_HEADERS:

            if header not in self.headers:
                missing.append(header)

        if missing:
            raise Exception(
                f"Header topilmadi: {missing}"
            )

    def get(self, row, column_name):

        column = self.headers[column_name]

        value = self.sheet.cell(
            row=row,
            column=column
        ).value

        if isinstance(value, str):
            value = value.strip()

        return value


    def clean_row(self, row):

        region = self.get(row, "BXM")
        branch = self.get(row, "Joylashgan joyi")
        address = self.get(row, "Yuridik manzili")

        if region:
            self.previous_region = region
        else:
            region = self.previous_region

        if branch:
            self.previous_branch = branch
        else:
            branch = self.previous_branch

        if address:
            self.previous_address = address
        else:
            address = self.previous_address

        return {

            "region": region,

            "branch": branch,

            "atm_type": self.get(row, "Bankomat turi"),

            "atm_model": self.get(row, "Bankomat modeli"),

            "status": self.get(row, "Holati"),

            "serial_number": str(
                self.get(row, "Seriya raqami") or ""
            ).strip(),

            "inventory_number": str(
                self.get(row, "Inventar raqami") or ""
            ).strip(),

            "merchant_id": str(
                self.get(row, "Merchant ID") or ""
            ).strip(),

            "terminal_id": str(
                self.get(row, "Terminal ID") or ""
            ).strip(),

            "legal_address": address,

            "expense": Decimal(
                self.get(row, "Ohirgi 3 oylik chiqim") or 0
            ),

            "income": Decimal(
                self.get(row, "Ohirgi 3 oylik daromad") or 0
            ),
        }


    def rows(self):

        for row in range(2, self.sheet.max_row + 1):

            serial = self.get(row, "Seriya raqami")

            if not serial:
                continue

            yield self.clean_row(row)


    def read(self):

        self.load_workbook()

        self.load_headers()

        for row in self.rows():

            yield row
