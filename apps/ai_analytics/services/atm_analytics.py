
from decimal import Decimal
from django.db.models import (
    Count,
    Q,
    Sum,
)
from django.db.models import (
    Count,
    Sum,
)

from apps.Bankomat_hisobot.models.ATMMonthlyStatistic import (
    ATMTURON,
    ATMMonthlyStatistic,
)


from apps.maintenance.models import MaintenanceItem


class ATMAnalyticsService:

    @staticmethod
    def count_by_region(
        region: str,
    ) -> dict:

        total = (
            ATMTURON.objects
            .filter(
                region__iexact=region
            )
            .count()
        )

        return {
            "region": region,
            "total_atms": total,
        }

    @staticmethod
    def revenue_by_region(
        region: str,
    ) -> dict:

        finance = (
            ATMMonthlyStatistic.objects
            .filter(
                atm__region__iexact=region
            )
            .aggregate(
                income=Sum("income"),
                expense=Sum("expense"),
            )
        )

        income = (
            finance["income"]
            or Decimal("0")
        )

        expense = (
            finance["expense"]
            or Decimal("0")
        )

        return {
            "region": region,
            "income": income,
            "expense": expense,
            "profit": income - expense,
        }

    @staticmethod
    def maintenance_cost_by_region(
            region: str,
    ) -> dict:
        maintenance = (
            MaintenanceItem.objects
            .filter(
                technical__atm__region__iexact=region
            )
            .aggregate(
                repair_count=Count("id"),
                repair_cost=Sum(
                    "total_with_vat"
                ),
            )
        )

        return {
            "region": region,
            "repair_count": (
                    maintenance["repair_count"]
                    or 0
            ),
            "repair_cost": (
                    maintenance["repair_cost"]
                    or Decimal("0")
            ),
        }

    @staticmethod
    def find_atm(
            serial_number: str | None = None,
            terminal_id: str | None = None,
            merchant_id: str | None = None,
            region: str | None = None,
            model: str | None = None,
            name: str | None = None,
    ) -> dict:

        queryset = (
            ATMTURON.objects
            .select_related("technical")
        )

        if serial_number:
            queryset = queryset.filter(
                technical__serial_number__icontains=
                serial_number.strip()
            )

        if terminal_id:
            queryset = queryset.filter(
                technical__terminal_id__icontains=
                terminal_id.strip()
            )

        if merchant_id:
            queryset = queryset.filter(
                technical__merchant_id__icontains=
                merchant_id.strip()
            )

        if region:
            queryset = queryset.filter(
                region__icontains=region.strip()
            )

        if model:
            queryset = queryset.filter(
                technical__model_name__icontains=
                model.strip()
            )

        if name:
            queryset = queryset.filter(
                name__icontains=name.strip()
            )

        items = queryset.values(
            "id",
            "name",
            "region",
            "is_active",
            "technical__serial_number",
            "technical__terminal_id",
            "technical__merchant_id",
            "technical__model_name",
            "technical__status",
            "technical__card_type",
        )

        return {
            "found": bool(items),
            "count": len(items),
            "items": list(items),
        }

    @staticmethod
    def performance_by_region(
            region: str,
    ) -> dict:

        atm_queryset = (
            ATMTURON.objects
            .filter(
                region__iexact=region
            )
        )

        total_atms = atm_queryset.count()

        finance = (
            ATMMonthlyStatistic.objects
            .filter(
                atm__region__iexact=region
            )
            .aggregate(
                income=Sum("income"),
                expense=Sum("expense"),
            )
        )

        income = (
                finance["income"]
                or Decimal("0")
        )

        expense = (
                finance["expense"]
                or Decimal("0")
        )

        maintenance = (
            MaintenanceItem.objects
            .filter(
                technical__atm__region__iexact=region
            )
            .aggregate(
                repair_count=Count("id"),
                repair_cost=Sum(
                    "total_with_vat"
                ),
            )
        )

        repair_count = (
                maintenance["repair_count"]
                or 0
        )

        repair_cost = (
                maintenance["repair_cost"]
                or Decimal("0")
        )

        return {
            "region": region,
            "total_atms": total_atms,
            "finance": {
                "income": income,
                "expense": expense,
                "profit": income - expense,
            },
            "maintenance": {
                "repair_count": repair_count,
                "repair_cost": repair_cost,
            },
        }

    @staticmethod
    def performance_by_atm(
            atm_id: int,
    ) -> dict:

        atm = (
            ATMTURON.objects
            .select_related("technical")
            .filter(
                id=atm_id
            )
            .first()
        )

        if not atm:
            return {
                "found": False,
                "message": "ATM topilmadi.",
            }

        finance = (
            ATMMonthlyStatistic.objects
            .filter(
                atm=atm
            )
            .aggregate(
                income=Sum("income"),
                expense=Sum("expense"),
            )
        )

        income = (
                finance["income"]
                or Decimal("0")
        )

        expense = (
                finance["expense"]
                or Decimal("0")
        )

        maintenance = (
            MaintenanceItem.objects
            .filter(
                technical=atm.technical
            )
            .aggregate(
                repair_count=Count("id"),
                repair_cost=Sum(
                    "total_with_vat"
                ),
            )
        )

        return {
            "found": True,

            "atm": {
                "id": atm.id,
                "name": atm.name,
                "region": atm.region,
                "is_active": atm.is_active,
                "serial_number": (
                    atm.technical.serial_number
                    if atm.technical
                    else None
                ),
                "terminal_id": (
                    atm.technical.terminal_id
                    if atm.technical
                    else None
                ),
                "merchant_id": (
                    atm.technical.merchant_id
                    if atm.technical
                    else None
                ),
                "model": (
                    atm.technical.model_name
                    if atm.technical
                    else None
                ),
                "status": (
                    atm.technical.status
                    if atm.technical
                    else None
                ),
                "card_type": (
                    atm.technical.card_type
                    if atm.technical
                    else None
                ),
            },

            "finance": {
                "income": income,
                "expense": expense,
                "profit": income - expense,
            },

            "maintenance": {
                "repair_count": (
                        maintenance["repair_count"]
                        or 0
                ),
                "repair_cost": (
                        maintenance["repair_cost"]
                        or Decimal("0")
                ),
            },
        }

    @staticmethod
    def monthly_trend(
            atm_id: int,
            months: int = 3,
    ) -> dict:

        statistics = (
            ATMMonthlyStatistic.objects
            .filter(
                atm_id=atm_id,
            )
            .exclude(
                income=0,
                expense=0,
            )
            .order_by(
                "-year",
                "-month",
            )[:months]
        )

        result = []

        for item in reversed(statistics):
            income = item.income or Decimal("0")
            expense = item.expense or Decimal("0")

            result.append({
                "year": item.year,
                "month": item.month,
                "income": income,
                "expense": expense,
                "profit": income - expense,
            })

        return {
            "atm_id": atm_id,
            "months": result,
        }

    @staticmethod
    def trend_analysis(
            atm_id: int,
            months: int = 3,
    ) -> dict:

        trend = ATMAnalyticsService.monthly_trend(
            atm_id=atm_id,
            months=months,
        )

        data = trend["months"]

        if len(data) < 2:
            return {
                "atm_id": atm_id,
                "status": "insufficient_data",
                "message": "Trend analysis uchun yetarli ma'lumot mavjud emas.",
            }

        first = data[0]
        last = data[-1]

        income_change = (
                last["income"] - first["income"]
        )

        expense_change = (
                last["expense"] - first["expense"]
        )

        profit_change = (
                last["profit"] - first["profit"]
        )

        def direction(value):

            if value > 0:
                return "increasing"

            if value < 0:
                return "decreasing"

            return "stable"

        return {
            "atm_id": atm_id,

            "period": {
                "from": {
                    "year": first["year"],
                    "month": first["month"],
                },

                "to": {
                    "year": last["year"],
                    "month": last["month"],
                },
            },

            "income": {
                "first": first["income"],
                "last": last["income"],
                "change": income_change,
                "trend": direction(income_change),
            },

            "expense": {
                "first": first["expense"],
                "last": last["expense"],
                "change": expense_change,
                "trend": direction(expense_change),
            },

            "profit": {
                "first": first["profit"],
                "last": last["profit"],
                "change": profit_change,
                "trend": direction(profit_change),
            },

            "monthly_data": data,
        }