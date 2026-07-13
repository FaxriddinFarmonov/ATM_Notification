import datetime
from pathlib import Path
from io import BytesIO
from collections import defaultdict

from apps.Bankomat_hisobot.models import ATMTechnical
from apps.maintenance.models import MaintenanceItem
from django.db.models import Sum
from openpyxl import Workbook
from openpyxl.styles import (
    Font,
    PatternFill,
    Alignment,
    Border,
    Side,
)
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image

from django.db.models import Prefetch

from ..models import (
    ATMTURON,
    ATMTechnical,
    ATMMonthlyStatistic,
    ATMYearStatistic,
)


class FullATMExcelExporter:
    """
    Export every ATM into one professional Excel report.

    Workbook:

        1. Summary
        2. ATM Information
        3. Monthly Statistics
        4. Year Statistics
    """

    def __init__(self):
        # Terminal ID -> Technical
        self.technical_cache = {
            tech.terminal_id.strip().upper(): tech
            for tech in ATMTechnical.objects.all()
        }

        # (technical_id, year, month) -> MaintenanceItem[]
        self.maintenance_cache = defaultdict(list)

        items = (
            MaintenanceItem.objects
            .select_related("technical")
            .exclude(technical=None)
        )

        for item in items:
            key = (
                item.technical_id,
                item.protocol_date.year,
                item.protocol_date.month,
            )

            self.maintenance_cache[key].append(item)
        self.workbook = Workbook()

        self.summary_sheet = self.workbook.active

        self.summary_sheet.title = "Summary"

        self.info_sheet = self.workbook.create_sheet(
            "ATM Information"
        )

        self.month_sheet = self.workbook.create_sheet(
            "Monthly Statistics"
        )

        self.year_sheet = self.workbook.create_sheet(
            "Year Statistics"
        )

        self.atms = (
            ATMTURON.objects
            .select_related("technical")
            .prefetch_related(
                Prefetch(
                    "monthly_statistics",
                    queryset=ATMMonthlyStatistic.objects.order_by(
                        "year",
                        "month",
                    ),
                ),
                Prefetch(
                    "year_statistics",
                    queryset=ATMYearStatistic.objects.order_by(
                        "year",
                    ),
                ),
            )
            .order_by(
                "region",
                "terminal_id",
            )
        )

    def export(self):

        self.prepare_document()

        self.add_logo()

        self.write_summary()

        self.write_information()

        self.write_month_statistics()

        self.write_year_statistics()

        self.style_workbook()

        self.auto_fit()

        self.freeze()

        return self.save()

    def add_logo(self):

        logo_path = Path("templates/turonbank.png")

        if not logo_path.exists():
            return

        logo = Image(str(logo_path))

        # Logo o'lchami (balansli)
        logo.width = 300
        logo.height = 45

        # Logo joylashuvi
        self.summary_sheet.add_image(
            logo,
            "A1",
        )

        # 1-qator balandligi
        self.summary_sheet.row_dimensions[1].height = 42
    def style_workbook(self):
        """
        Workbook'ni professional ko'rinishga keltiradi.
        """

        # Ranglar
        header_fill = PatternFill(
            fill_type="solid",
            start_color="1F4E78",
            end_color="1F4E78",
        )

        summary_fill = PatternFill(
            fill_type="solid",
            start_color="DCEEFF",
            end_color="DCEEFF",
        )

        white_fill = PatternFill(fill_type=None)

        header_font = Font(
            bold=True,
            color="FFFFFF",
        )

        bold_font = Font(
            bold=True,
        )

        thin = Side(
            style="thin",
            color="D9D9D9",
        )

        border = Border(
            left=thin,
            right=thin,
            top=thin,
            bottom=thin,
        )

        for sheet in self.workbook.worksheets:

            # Border + Alignment
            for row in sheet.iter_rows():

                for cell in row:
                    cell.border = border
                    cell.alignment = Alignment(
                        vertical="center"
                    )

            # ===========================
            # SUMMARY SHEET
            # ===========================

            if sheet.title == "Summary":

                # 1-qator mutlaqo oq bo'lsin
                for cell in sheet[1]:
                    cell.fill = white_fill
                    cell.font = bold_font
                    cell.alignment = Alignment(
                        horizontal="left",
                        vertical="center",
                    )

                # Dashboard chap ustuni
                for row in range(8, sheet.max_row + 1):
                    sheet.cell(row, 1).fill = summary_fill
                    sheet.cell(row, 1).font = bold_font

                    sheet.cell(row, 2).font = Font(
                        bold=True,
                    )

                continue

            # ===========================
            # QOLGAN SHEETLAR
            # ===========================

            for cell in sheet[1]:
                cell.fill = header_fill

                cell.font = header_font

                cell.alignment = Alignment(
                    horizontal="center",
                    vertical="center",
                )

            # Header balandligi
            sheet.row_dimensions[1].height = 24
    def prepare_document(self):
        props = self.workbook.properties

        props.creator = "Turonbank"

        props.company = "Turonbank"

        props.title = "ATM Full Report"

        props.subject = "ATM Statistics"

        props.description = (
            "Complete ATM Report"
        )

        props.created = datetime.datetime.now()

    def save(self):
        output = BytesIO()

        self.workbook.save(output)

        output.seek(0)

        return output

    def freeze(self):
        self.summary_sheet.freeze_panes = "A2"

        self.info_sheet.freeze_panes = "A2"

        self.month_sheet.freeze_panes = "A2"

        self.year_sheet.freeze_panes = "A2"

    from openpyxl.utils import get_column_letter

    def auto_fit(self):

        for sheet in self.workbook.worksheets:

            for column in sheet.columns:

                length = 0

                letter = get_column_letter(
                    column[0].column
                )

                for cell in column:

                    if cell.value is None:
                        continue

                    length = max(
                        length,
                        len(str(cell.value)),
                    )

                sheet.column_dimensions[
                    letter
                ].width = min(length + 4, 40)

    def write_information(self):

        ws = self.info_sheet

        headers = [
            "Region",
            "ATM Name",
            "Address",
            "Processing",
            "ATM Model",
            "Serial Number",
            "Terminal ID",
            "Merchant ID",
            "Status",
            "Inventory Number",
            "23510 Account",
            "45265 Account",
        ]

        ws.append(headers)

        for atm in self.atms:
            tech = getattr(atm, "technical", None)

            ws.append([
                atm.region,
                atm.name,
                atm.address,
                atm.card_type,
                atm.model,
                tech.serial_number if tech else "",
                atm.terminal_id,
                tech.merchant_id if tech else "",
                tech.status if tech else "",
                tech.inventory_number if tech else "",
                tech.account_23510 if tech else "",
                tech.account_45265 if tech else "",
            ])


    def write_month_statistics(self):

        ws = self.month_sheet

        ws.append([
            "Terminal ID",
            "Processing",
            "Year",
            "Month",

            "Income",
            "Cash Withdraw",

            "Repair Cost",

            "Quantity",

            "Status",
            "Serial Number",
            "Merchant ID",
            "Inventory Number",

            "ATM Name",
            "Region",
        ])

        months = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December",
        }

        statistics = (
            ATMMonthlyStatistic.objects
            .select_related(
                "atm",
                "atm__technical",
            )
            .order_by(
                "atm__region",
                "atm__terminal_id",
                "year",
                "month",
            )
        )

        for item in statistics:
            tech = self.technical_cache.get(
                item.atm.terminal_id.strip().upper()
            )

            if tech:

                items = self.maintenance_cache.get(
                    (
                        tech.id,
                        item.year,
                        item.month,
                    ),
                    [],
                )

            else:

                items = []
            repair_cost = 0
            vat = 0
            quantity = 0



            for i in items:

                repair_cost += i.total_with_vat
                quantity += i.quantity

            ws.append([
                item.atm.terminal_id,
                item.atm.card_type,

                item.year,
                months[item.month],

                float(item.income),
                float(item.expense),

                float(repair_cost),

                float(quantity),

                tech.status if tech else "",
                tech.serial_number if tech else "",
                tech.merchant_id if tech else "",
                tech.inventory_number if tech else "",

                item.atm.name,
                item.atm.region,
            ])

    def write_year_statistics(self):

        ws = self.year_sheet

        ws.append([
            "Terminal ID",
            "Processing",
            "Year",

            "Income",
            "Cash Withdraw",

            "Year Repair Cost",

            "Status",
            "Serial Number",
            "Merchant ID",
            "Inventory Number",

            "ATM Name",
            "Region",
        ])

        # -------------------------------
        # Technical cache (Terminal ID -> Technical)
        # -------------------------------
        technical_cache = {
            tech.terminal_id: tech
            for tech in ATMTechnical.objects.all()
        }

        # -------------------------------
        # Yearly maintenance cache
        # (serial_number, year) -> total repair
        # -------------------------------
        maintenance_cache = defaultdict(float)

        for item in MaintenanceItem.objects.exclude(serial_number=""):
            key = (
                item.serial_number.strip().upper(),
                item.protocol_date.year,
            )

            maintenance_cache[key] += float(item.total_with_vat)

        # -------------------------------
        # Year statistics
        # -------------------------------
        statistics = (
            ATMYearStatistic.objects
            .select_related("atm")
            .order_by(
                "atm__region",
                "atm__terminal_id",
                "year",
            )
        )

        for item in statistics:

            tech = technical_cache.get(
                item.atm.terminal_id
            )

            repair = 0

            if tech and tech.serial_number:
                repair = maintenance_cache.get(
                    (
                        tech.serial_number.strip().upper(),
                        item.year,
                    ),
                    0,
                )

            ws.append([
                item.atm.terminal_id,
                item.card_type,

                item.year,

                float(item.income),
                float(item.expense),

                float(repair),

                tech.status if tech else "",
                tech.serial_number if tech else "",
                tech.merchant_id if tech else "",
                tech.inventory_number if tech else "",

                item.atm.name,
                item.atm.region,
            ])

    def write_summary(self):

        ws = self.summary_sheet

        # ======================================================
        # TITLE
        # ======================================================

        ws.merge_cells("A1:B1")
        title = ws["A1"]
        ws.row_dimensions[1].height = 30

        title.font = Font(
            size=18,
            bold=True,
            color="FFFFFF",
        )

        title.fill = PatternFill(
            fill_type="solid",
            start_color="1F4E78",
            end_color="1F4E78",
        )

        title.alignment = Alignment(
            horizontal="center",
            vertical="center",
        )

        # ======================================================
        # REPORT INFO
        # ======================================================
        ws["A2"] = "Generated"
        ws["B2"] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

        ws["A3"] = "Generated By"
        ws["B3"] = "Turonbank Monitoring System"

        # ======================================================
        # SUMMARY
        # ======================================================

        summary = [

            (
                "Total ATM",
                ATMTURON.objects.count(),
            ),

            (
                "Technical Linked",
                ATMTechnical.objects.filter(
                    atm__isnull=False
                ).count(),
            ),

            (
                "Active ATM",
                ATMTURON.objects.filter(
                    is_active=True
                ).count(),
            ),

            (
                "UZCARD ATM",
                ATMTURON.objects.filter(
                    card_type="UZCARD"
                ).count(),
            ),

            (
                "HUMO ATM",
                ATMTURON.objects.filter(
                    card_type="HUMO"
                ).count(),
            ),

            (
                "Regions",
                ATMTURON.objects.values(
                    "region"
                ).distinct().count(),
            ),

            (
                "Monthly Statistics",
                ATMMonthlyStatistic.objects.count(),
            ),

            (
                "Year Statistics",
                ATMYearStatistic.objects.count(),
            ),

        ]

        row = 8

        header_fill = PatternFill(
            fill_type="solid",
            start_color="D9EAF7",
            end_color="D9EAF7",
        )

        border = Border(
            left=Side(style="thin"),
            right=Side(style="thin"),
            top=Side(style="thin"),
            bottom=Side(style="thin"),
        )

        for title, value in summary:
            name_cell = ws.cell(
                row=row,
                column=1,
            )

            value_cell = ws.cell(
                row=row,
                column=2,
            )

            name_cell.value = title
            value_cell.value = value

            name_cell.font = Font(bold=True)

            name_cell.fill = header_fill

            name_cell.border = border
            value_cell.border = border

            name_cell.alignment = Alignment(
                vertical="center",
            )

            value_cell.alignment = Alignment(
                horizontal="center",
                vertical="center",
            )

            row += 1