import requests
from collections import defaultdict
from decimal import Decimal
from collections import defaultdict
from decimal import Decimal

from django.db.models import Sum
from collections import defaultdict
from decimal import Decimal

from django.db.models import Sum
from collections import defaultdict
from decimal import Decimal

from django.db.models import Sum
from collections import defaultdict
from decimal import Decimal

from django.db.models import Sum
from collections import defaultdict
from decimal import Decimal

from django.db.models import Sum

from apps.Bankomat_hisobot.models.ATMMonthlyStatistic import (
    ATMTURON,
    ATMMonthlyStatistic,
    ATMYearStatistic,
)

from apps.Bankomat_hisobot.models.ATMServiceContract import (
    ATMServiceContract,
    ATMServicePayment,
)

from apps.Bankomat_hisobot.models.full_models import (
    ATMTechnical,
)

from apps.maintenance.models import MaintenanceItem



class RegionAnalyticsService:

    def __init__(
            self,
            region,
            start_year=None,
            end_year=None,
            start_month=None,
            end_month=None,
    ):
        self.region = region

        self.start_year = (
            int(start_year)
            if start_year
            else None
        )

        self.end_year = (
            int(end_year)
            if end_year
            else None
        )

        self.start_month = (
            int(start_month)
            if start_month
            else None
        )

        self.end_month = (
            int(end_month)
            if end_month
            else None
        )
    MONEY_MULTIPLIER = Decimal("1000")

    @staticmethod
    def decimal(value):
        if value is None:
            return Decimal("0")

        return Decimal(str(value))

    @staticmethod
    def money(value):
        return float(
            RegionAnalyticsService.decimal(value) * RegionAnalyticsService.MONEY_MULTIPLIER
        )

    @staticmethod
    def percentage(current, previous):

        current = RegionAnalyticsService.decimal(current)
        previous = RegionAnalyticsService.decimal(previous)

        if previous == 0:
            return 0

        return float(
            ((current - previous) / previous) * 100
        )

    def _atm_ranking(self, atms, monthly_qs):
        """
        Viloyat ichidagi ATMlarni daromad va sof natija
        bo'yicha reyting qiladi.
        """

        rows = (
            monthly_qs
            .values(
                "atm_id",
                "atm__terminal_id",
                "atm__name",
            )
            .annotate(
                income_total=Sum("income"),
                expense_total=Sum("expense"),
            )
            .order_by("-income_total")
        )

        result = []

        for index, row in enumerate(rows, start=1):
            income = (
                    row["income_total"]
                    or Decimal("0")
            ) * RegionAnalyticsService.MONEY_MULTIPLIER

            expense = (
                    row["expense_total"]
                    or Decimal("0")
            ) * RegionAnalyticsService.MONEY_MULTIPLIER

            net_result = income - expense

            result.append({
                "rank": index,
                "atm_id": row["atm_id"],
                "terminal_id": row["atm__terminal_id"],
                "name": row["atm__name"],
                "income": float(income),
                "expense": float(expense),
                "net_result": float(net_result),
            })

        return result
    def _financial(self, monthly_qs):

        total_income = (
                monthly_qs.aggregate(
                    total=Sum("income")
                )["total"]
                or Decimal("0")
        ) * RegionAnalyticsService.MONEY_MULTIPLIER

        total_expense = (
                monthly_qs.aggregate(
                    total=Sum("expense")
                )["total"]
                or Decimal("0")
        ) * RegionAnalyticsService.MONEY_MULTIPLIER

        net_result = total_income - total_expense

        return {
            "income": float(total_income),
            "expense": float(total_expense),
            "net_result": float(net_result),
        }
    def _maintenance(self, atms):
        qs = MaintenanceItem.objects.filter(
            technical__atm__in=atms
        )

        total = qs.aggregate(
            total=Sum("total_with_vat")
        )["total"] or Decimal("0")

        return {
            "items_count": qs.count(),
            "total_cost": float(total),
        }
    def _technical(self, atms):
        total = atms.count()

        active = atms.filter(
            is_active=True
        ).count()

        inactive = atms.filter(
            is_active=False
        ).count()

        technical_qs = ATMTechnical.objects.filter(
            atm__in=atms
        )

        working = technical_qs.filter(
            status="SOZ"
        ).count()

        broken = technical_qs.filter(
            status="NOSOZ"
        ).count()

        return {
            "total_atms": total,
            "active_atms": active,
            "inactive_atms": inactive,
            "technical_data_count": technical_qs.count(),
            "working": working,
            "broken": broken,
        }
    def get_atms(self):

        return ATMTURON.objects.filter(
            region=self.region
        )

    def build(self):

        # ATMMonthlyStatistic qaysi ATMTURON bilan bog'langan bo'lsa,
        # aynan o'sha model ishlatiladi
        atm_model = ATMMonthlyStatistic._meta.get_field("atm").remote_field.model

        atms = atm_model.objects.filter(
            region=self.region
        )

        if not atms.exists():
            return {
                "region": self.region,
                "atm_count": 0,
                "message": "Bu viloyatda ATM topilmadi.",
            }

        if self.start_year and self.end_year:

            monthly = ATMMonthlyStatistic.objects.filter(
                atm__in=atms
            )

            # YIL FILTER
            if self.start_year:
                monthly = monthly.filter(
                    year__gte=self.start_year
                )

            if self.end_year:
                monthly = monthly.filter(
                    year__lte=self.end_year
                )

            # OY FILTER
            if self.start_month:
                monthly = monthly.filter(
                    month__gte=self.start_month
                )

            if self.end_month:
                monthly = monthly.filter(
                    month__lte=self.end_month
                )

        else:

            monthly = ATMMonthlyStatistic.objects.filter(
                atm__in=atms
            )

        return {
            "region": self.region,

            "atm_count": atms.count(),

            "technical": self._technical(
                atms
            ),

            "financial": self._financial(
                monthly
            ),

            "profitability": self._profitability(
                atms,
                monthly,
            ),

            "yearly": self._yearly(
                monthly,
                atms,
            ),

            "monthly": self._monthly(
                monthly,
                atms,
            ),

            "services": self._services(
                atms
            ),

            "maintenance": self._maintenance(
                atms
            ),

            "atm_ranking": self._atm_ranking(
                atms,
                monthly,
            ),
        }
    def build_financial(self, atm_ids):

        statistics = ATMMonthlyStatistic.objects.filter(
            atm_id__in=atm_ids
        ).values(
            "year",
            "month",
        ).annotate(
            income=Sum("income"),
            cash_withdrawal=Sum("expense"),
        ).order_by(
            "year",
            "month",
        )

        yearly = defaultdict(
            lambda: {
                "income": Decimal("0"),
                "cash_withdrawal": Decimal("0"),
            }
        )

        monthly = []

        for item in statistics:

            year = item["year"]
            month = item["month"]

            income = self.decimal(
                item["income"]
            )

            cash_withdrawal = self.decimal(
                item["cash_withdrawal"]
            )

            yearly[year]["income"] += income
            yearly[year]["cash_withdrawal"] += cash_withdrawal

            monthly.append({
                "year": year,
                "month": month,
                "income": self.money(income),
                "cash_withdrawal": self.money(
                    cash_withdrawal
                ),
            })

        years = []

        previous = None

        for year in sorted(yearly.keys()):

            income = yearly[year]["income"]
            cash_withdrawal = yearly[year][
                "cash_withdrawal"
            ]

            item = {
                "year": year,

                "income": self.money(
                    income
                ),

                "cash_withdrawal": self.money(
                    cash_withdrawal
                ),
            }

            if previous:

                item["income_growth_percent"] = (
                    self.percentage(
                        income,
                        previous["income"]
                    )
                )

                item["cash_withdrawal_growth_percent"] = (
                    self.percentage(
                        cash_withdrawal,
                        previous["cash_withdrawal"]
                    )
                )

            else:

                item["income_growth_percent"] = None
                item["cash_withdrawal_growth_percent"] = None

            years.append(item)

            previous = {
                "income": income,
                "cash_withdrawal": cash_withdrawal,
            }

        total_income = sum(
            item["income"]
            for item in yearly.values()
        )

        total_cash_withdrawal = sum(
            item["cash_withdrawal"]
            for item in yearly.values()
        )

        return {
            "total_income": self.money(
                total_income
            ),

            "total_cash_withdrawal": self.money(
                total_cash_withdrawal
            ),

            "yearly": years,

            "monthly": monthly,
        }

    def build_service_costs(self, atm_ids):

        contracts = ATMServiceContract.objects.filter(
            atm_id__in=atm_ids
        )

        btech = contracts.aggregate(
            total=Sum("btech_monthly_fee")
        )["total"] or Decimal("0")

        glob = contracts.aggregate(
            total=Sum("glob_monthly_fee")
        )["total"] or Decimal("0")

        payments = ATMServicePayment.objects.filter(
            contract__atm_id__in=atm_ids
        )

        incassation = payments.filter(
            payment_type=ATMServicePayment.PaymentType.INCASSATION
        ).aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0")

        rent = payments.filter(
            payment_type=ATMServicePayment.PaymentType.RENT
        ).aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0")

        electricity = payments.filter(
            payment_type=ATMServicePayment.PaymentType.ELECTRICITY
        ).aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0")

        return {
            "btech_monthly_fee": self.money(
                btech
            ),

            "glob_monthly_fee": self.money(
                glob
            ),

            "incassation": self.money(
                incassation
            ),

            "rent": self.money(
                rent
            ),

            "electricity": self.money(
                electricity
            ),
        }

    def build_maintenance(self, atm_ids):

        items = MaintenanceItem.objects.filter(
            technical__atm_id__in=atm_ids
        )

        total = items.aggregate(
            total=Sum("total_with_vat")
        )["total"] or Decimal("0")

        return {
            "total": float(total),
            "items_count": items.count(),
        }

    def build_technical(self, atm_ids):

        technical = ATMTechnical.objects.filter(
            atm_id__in=atm_ids
        )

        total = technical.count()

        good = technical.filter(
            status="SOZ"
        ).count()

        bad = technical.filter(
            status="NOSOZ"
        ).count()

        return {
            "total": total,
            "good": good,
            "bad": bad,

            "failure_rate_percent": (
                round(
                    (bad / total) * 100,
                    2
                )
                if total
                else 0
            ),
        }
    def _services(self, atms):

        # =========================
        # 1. TANLANGAN OYLAR SONI
        # =========================

        if self.start_year and self.end_year:
            months_count = (
                (self.end_year - self.start_year + 1) * 12
            )
        else:
            months_count = 12

        # =========================
        # 2. BTECH + GLOB
        # =========================

        contracts = atms.filter(
            service_contract__isnull=False
        ).select_related(
            "service_contract"
        )

        btech_monthly = Decimal("0")
        glob_monthly = Decimal("0")

        for atm in contracts:

            contract = atm.service_contract

            btech_monthly += (
                contract.btech_monthly_fee
                or Decimal("0")
            )

            glob_monthly += (
                contract.glob_monthly_fee
                or Decimal("0")
            )

        btech_total = (
            btech_monthly * months_count
        )

        glob_total = (
            glob_monthly * months_count
        )

        # =========================
        # 3. INCASSATION / RENT /
        #    ELECTRICITY
        # =========================

        payments = ATMServicePayment.objects.filter(
            contract__atm__in=atms
        )

        if self.start_year and self.end_year:

            payments = payments.filter(
                year__gte=self.start_year,
                year__lte=self.end_year,
            )

        payment_data = payments.values(
            "payment_type"
        ).annotate(
            total=Sum("amount")
        )

        incassation = Decimal("0")
        rent = Decimal("0")
        electricity = Decimal("0")

        for item in payment_data:

            payment_type = item["payment_type"]

            total = (
                item["total"]
                or Decimal("0")
            )

            if payment_type == "INCASSATION":

                incassation += total

            elif payment_type == "RENT":

                rent += total

            elif payment_type == "ELECTRICITY":

                electricity += total

        # =========================
        # 4. NATIJA
        # =========================

        return {
            "btech": float(btech_total),
            "glob": float(glob_total),

            "incassation": float(
                incassation
            ),

            "rent": float(
                rent
            ),

            "electricity": float(
                electricity
            ),

            "total_service_cost": float(
                btech_total
                + glob_total
                + incassation
                + rent
                + electricity
            ),
        }
    def _maintenance(self, atms):

        items = MaintenanceItem.objects.filter(
            technical__atm__in=atms
        )

        # =========================
        # YIL FILTRI
        # =========================

        if self.start_year and self.end_year:

            items = items.filter(
                protocol_date__year__gte=self.start_year,
                protocol_date__year__lte=self.end_year,
            )

        # =========================
        # UMUMIY MAINTENANCE
        # =========================

        total_result = items.aggregate(
            total=Sum("total_with_vat")
        )

        total = (
            total_result["total"]
            or Decimal("0")
        )

        # =========================
        # PARTLAR / XIZMATLAR
        # =========================

        parts = items.values(
            "part_name"
        ).annotate(
            total=Sum("total_with_vat")
        ).order_by(
            "-total"
        )

        parts_result = []

        for item in parts:

            parts_result.append({
                "part_name": item["part_name"],
                "total": float(
                    item["total"] or Decimal("0")
                ),
            })

        # =========================
        # ATM BO'YICHA
        # =========================

        atm_data = items.values(
            "technical__atm__terminal_id",
            "technical__atm__address",
        ).annotate(
            total=Sum("total_with_vat")
        ).order_by(
            "-total"
        )

        atm_result = []

        for item in atm_data:

            atm_result.append({
                "terminal_id": (
                    item[
                        "technical__atm__terminal_id"
                    ]
                ),

                "address": (
                    item[
                        "technical__atm__address"
                    ]
                ),

                "total": float(
                    item["total"]
                    or Decimal("0")
                ),
            })

        # =========================
        # NATIJA
        # =========================

        return {
            "total": float(total),

            "parts": parts_result,

            "by_atm": atm_result,
        }

    def _profitability(self, atms, monthly):
        """
        Viloyatning umumiy moliyaviy samaradorligi.
        """

        # =========================
        # DAROMAD
        # =========================

        income_result = monthly.aggregate(
            total=Sum("income")
        )

        income = (
            income_result["total"]
            or Decimal("0")
        )

        # =========================
        # SERVICE XARAJATLARI
        # =========================

        services = self._services(atms)

        btech = Decimal(
            str(services["btech"])
        )

        glob = Decimal(
            str(services["glob"])
        )

        incassation = Decimal(
            str(services["incassation"])
        )

        rent = Decimal(
            str(services["rent"])
        )

        electricity = Decimal(
            str(services["electricity"])
        )

        # =========================
        # MAINTENANCE
        # =========================

        maintenance = self._maintenance(atms)

        maintenance_total = Decimal(
            str(maintenance["total"])
        )

        # =========================
        # JAMI XARAJAT
        # =========================

        total_expense = (
            btech
            + glob
            + incassation
            + rent
            + electricity
            + maintenance_total
        )

        # =========================
        # SOF NATIJA
        # =========================

        net_result = (
            income - total_expense
        )

        # =========================
        # RENTABELLIK
        # =========================

        profitability_percentage = 0

        if income:

            profitability_percentage = round(
                (
                    net_result / income
                ) * 100,
                2,
            )

        # =========================
        # XARAJATLAR ULUSHI
        # =========================

        expense_share = {}

        if total_expense:

            expense_share = {
                "btech": round(
                    float(
                        btech
                        / total_expense
                        * 100
                    ),
                    2,
                ),

                "glob": round(
                    float(
                        glob
                        / total_expense
                        * 100
                    ),
                    2,
                ),

                "incassation": round(
                    float(
                        incassation
                        / total_expense
                        * 100
                    ),
                    2,
                ),

                "rent": round(
                    float(
                        rent
                        / total_expense
                        * 100
                    ),
                    2,
                ),

                "electricity": round(
                    float(
                        electricity
                        / total_expense
                        * 100
                    ),
                    2,
                ),

                "maintenance": round(
                    float(
                        maintenance_total
                        / total_expense
                        * 100
                    ),
                    2,
                ),
            }

        return {
            "income": float(income),

            "total_expense": float(
                total_expense
            ),

            "net_result": float(
                net_result
            ),

            "profitability_percentage": (
                profitability_percentage
            ),

            "expense_share": expense_share,
        }

    def _yearly(self, monthly, atms):

        yearly_data = defaultdict(
            lambda: {
                "income": Decimal("0"),
                "cash_withdrawal": Decimal("0"),
                "btech": Decimal("0"),
                "glob": Decimal("0"),
                "incassation": Decimal("0"),
                "rent": Decimal("0"),
                "electricity": Decimal("0"),
                "maintenance": Decimal("0"),
                "total_expense": Decimal("0"),
                "net_result": Decimal("0"),
            }
        )

        # ==========================================
        # OYLIK MA'LUMOTLARDAN YILLIK YIG'ISH
        # ==========================================

        statistics = monthly.order_by(
            "year",
            "month",
        )

        for item in statistics:

            year = item.year

            income = (
                item.income
                or Decimal("0")
            )

            cash_withdrawal = (
                item.expense
                or Decimal("0")
            )

            # Shu oy xarajatlarini olamiz
            costs = self._period_costs(
                atms,
                item.year,
                item.month,
            )

            yearly_data[year]["income"] += income

            yearly_data[year]["cash_withdrawal"] += (
                cash_withdrawal
            )

            yearly_data[year]["btech"] += Decimal(str(costs["btech"]))
            yearly_data[year]["glob"] += Decimal(str(costs["glob"]))
            yearly_data[year]["incassation"] += Decimal(str(costs["incassation"]))
            yearly_data[year]["rent"] += Decimal(str(costs["rent"]))
            yearly_data[year]["electricity"] += Decimal(str(costs["electricity"]))
            yearly_data[year]["maintenance"] += Decimal(str(costs["maintenance"]))
            yearly_data[year]["total_expense"] += Decimal(str(costs["total_expense"]))
            yearly_data[year]["net_result"] += (
                income - Decimal(str(costs["total_expense"]))
            )

        # ==========================================
        # YILLIK NATIJA
        # ==========================================

        result = []

        previous = None

        for year in sorted(yearly_data.keys()):

            data = yearly_data[year]

            income = data["income"]

            cash_withdrawal = (
                data["cash_withdrawal"]
            )

            btech = data["btech"]
            glob = data["glob"]
            incassation = data["incassation"]
            rent = data["rent"]
            electricity = data["electricity"]
            maintenance = data["maintenance"]

            total_expense = (
                data["total_expense"]
            )

            net_result = (
                data["net_result"]
            )

            # ======================================
            # O'SISH FOIZLARI
            # ======================================

            income_growth = None
            withdrawal_growth = None
            expense_growth = None
            net_growth = None

            if previous:

                previous_income = (
                    previous["income"]
                )

                previous_withdrawal = (
                    previous["cash_withdrawal"]
                )

                previous_expense = (
                    previous["total_expense"]
                )

                previous_net = (
                    previous["net_result"]
                )

                if previous_income:

                    income_growth = round(
                        (
                            (
                                income
                                - previous_income
                            )
                            / previous_income
                        ) * 100,
                        2,
                    )

                if previous_withdrawal:

                    withdrawal_growth = round(
                        (
                            (
                                cash_withdrawal
                                - previous_withdrawal
                            )
                            / previous_withdrawal
                        ) * 100,
                        2,
                    )

                if previous_expense:

                    expense_growth = round(
                        (
                            (
                                total_expense
                                - previous_expense
                            )
                            / previous_expense
                        ) * 100,
                        2,
                    )

                if previous_net:

                    net_growth = round(
                        (
                            (
                                net_result
                                - previous_net
                            )
                            / abs(previous_net)
                        ) * 100,
                        2,
                    )

            # ======================================
            # NATIJA
            # ======================================

            result.append({

                "year": year,

                "income": float(
                    income
                ),

                "cash_withdrawal": float(
                    cash_withdrawal
                ),

                "expenses": {

                    "btech": float(
                        btech
                    ),

                    "glob": float(
                        glob
                    ),

                    "incassation": float(
                        incassation
                    ),

                    "rent": float(
                        rent
                    ),

                    "electricity": float(
                        electricity
                    ),

                    "maintenance": float(
                        maintenance
                    ),

                    "total": float(
                        total_expense
                    ),
                },

                "net_result": float(
                    net_result
                ),

                "income_growth_percentage": (
                    income_growth
                ),

                "cash_withdrawal_growth_percentage": (
                    withdrawal_growth
                ),

                "expense_growth_percentage": (
                    expense_growth
                ),

                "net_result_growth_percentage": (
                    net_growth
                ),
            })

            previous = {

                "income": income,

                "cash_withdrawal": (
                    cash_withdrawal
                ),

                "total_expense": (
                    total_expense
                ),

                "net_result": net_result,
            }

        return result
    def _monthly(self, monthly, atms):

        result = []

        previous = None

        month_names = {
            1: "Yanvar",
            2: "Fevral",
            3: "Mart",
            4: "Aprel",
            5: "May",
            6: "Iyun",
            7: "Iyul",
            8: "Avgust",
            9: "Sentabr",
            10: "Oktabr",
            11: "Noyabr",
            12: "Dekabr",
        }

        statistics = monthly.order_by(
            "year",
            "month",
        )

        for item in statistics:

            income = (
                item.income
                or Decimal("0")
            )

            cash_withdrawal = (
                item.expense
                or Decimal("0")
            )

            # =========================
            # OYLIK XARAJATLAR
            # =========================

            costs = self._period_costs(
                atms,
                item.year,
                item.month,
            )

            # =========================
            # SOF NATIJA
            # =========================

            net_result = (
                income
                - costs["total_expense"]
            )

            # =========================
            # OYLIK O'SISH
            # =========================

            income_growth = None
            withdrawal_growth = None
            net_growth = None

            if previous:

                previous_income = (
                    previous["income"]
                )

                previous_withdrawal = (
                    previous["cash_withdrawal"]
                )

                previous_net = (
                    previous["net_result"]
                )

                if previous_income:

                    income_growth = round(
                        (
                            (
                                income
                                - previous_income
                            )
                            / previous_income
                        ) * 100,
                        2,
                    )

                if previous_withdrawal:

                    withdrawal_growth = round(
                        (
                            (
                                cash_withdrawal
                                - previous_withdrawal
                            )
                            / previous_withdrawal
                        ) * 100,
                        2,
                    )

                if previous_net:

                    net_growth = round(
                        (
                            (
                                net_result
                                - previous_net
                            )
                            / abs(previous_net)
                        ) * 100,
                        2,
                    )

            # =========================
            # NATIJA
            # =========================

            result.append({

                "year": item.year,

                "month": item.month,

                "month_name": month_names.get(
                    item.month,
                    str(item.month),
                ),

                "income": float(
                    income
                ),

                "cash_withdrawal": float(
                    cash_withdrawal
                ),

                "expenses": {
                    "btech": float(
                        costs["btech"]
                    ),

                    "glob": float(
                        costs["glob"]
                    ),

                    "incassation": float(
                        costs["incassation"]
                    ),

                    "rent": float(
                        costs["rent"]
                    ),

                    "electricity": float(
                        costs["electricity"]
                    ),

                    "maintenance": float(
                        costs["maintenance"]
                    ),

                    "total": float(
                        costs["total_expense"]
                    ),
                },

                "net_result": float(
                    net_result
                ),

                "income_growth_percentage": (
                    income_growth
                ),

                "cash_withdrawal_growth_percentage": (
                    withdrawal_growth
                ),

                "net_result_growth_percentage": (
                    net_growth
                ),
            })

            previous = {

                "income": income,

                "cash_withdrawal": (
                    cash_withdrawal
                ),

                "net_result": net_result,
            }

        return result
    def _period_costs(self, atms, year, month):
        """
        Berilgan yil va oy uchun:
        BTECH
        GLOB
        INCASSATION
        RENT
        ELECTRICITY
        MAINTENANCE
        hisoblaydi.
        """

        # =========================
        # BTECH + GLOB
        # =========================

        contracts = (
            atms
            .filter(
                service_contract__isnull=False
            )
            .select_related(
                "service_contract"
            )
        )

        btech = Decimal("0")
        glob = Decimal("0")

        for atm in contracts:

            contract = atm.service_contract

            btech += (
                contract.btech_monthly_fee
                or Decimal("0")
            )

            glob += (
                contract.glob_monthly_fee
                or Decimal("0")
            )

        # =========================
        # SERVICE PAYMENTS
        # =========================

        payments = ATMServicePayment.objects.filter(
            contract__atm__in=atms,
            year=year,
            month=month,
        )

        payment_data = payments.values(
            "payment_type"
        ).annotate(
            total=Sum("amount")
        )

        incassation = Decimal("0")
        rent = Decimal("0")
        electricity = Decimal("0")

        for item in payment_data:

            payment_type = item["payment_type"]

            total = (
                item["total"]
                or Decimal("0")
            )

            if payment_type == "INCASSATION":

                incassation += total

            elif payment_type == "RENT":

                rent += total

            elif payment_type == "ELECTRICITY":

                electricity += total

        # =========================
        # MAINTENANCE
        # =========================

        maintenance_result = (
            MaintenanceItem.objects
            .filter(
                technical__atm__in=atms,
                protocol_date__year=year,
                protocol_date__month=month,
            )
            .aggregate(
                total=Sum("total_with_vat")
            )
        )

        maintenance = (
            maintenance_result["total"]
            or Decimal("0")
        )

        # =========================
        # TOTAL EXPENSE
        # =========================

        mult = Decimal("1000")
        btech_real = btech * mult
        glob_real = glob * mult
        incassation_real = incassation * mult
        rent_real = rent * mult
        electricity_real = electricity * mult

        total_expense = (
            btech_real
            + glob_real
            + incassation_real
            + rent_real
            + electricity_real
            + maintenance
        )

        return {
            "btech": float(btech_real),
            "glob": float(glob_real),
            "incassation": float(incassation_real),
            "rent": float(rent_real),
            "electricity": float(electricity_real),
            "maintenance": float(maintenance),
            "total_expense": float(total_expense),
        }

