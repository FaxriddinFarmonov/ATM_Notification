from django.db.models import Count, Sum, Q
from .charts import DashboardChartService
from apps.Bankomat_hisobot.models.ATMMonthlyStatistic import (
    ATMTURON,
    ATMMonthlyStatistic,
)
from apps.maintenance.models import MaintenanceItem

from django.db.models import Count, Q

from apps.Bankomat_hisobot.models.ATMMonthlyStatistic import ATMTURON

from .charts import DashboardChartService


class DashboardService:
    MONEY_MULTIPLIER = 1000

    @staticmethod
    def money(value):
        return (value or 0) * DashboardService.MONEY_MULTIPLIER

    @staticmethod
    def summary():

        queryset = (
            ATMTURON.objects
            .select_related("technical")
        )

        total = queryset.count()

        active = queryset.filter(
            is_active=True
        ).count()

        return {

            "total_atms": total,

            "active": active,

            "inactive": total - active,

            "soz": queryset.filter(
                technical__status="SOZ"
            ).count(),

            "nosoz": queryset.filter(
                technical__status="NOSOZ"
            ).count(),

            "uzcard": queryset.filter(
                technical__card_type="UZCARD"
            ).count(),

            "humo": queryset.filter(
                technical__card_type="HUMO"
            ).count(),

        }
    @staticmethod
    def finance():

        finance = ATMMonthlyStatistic.objects.aggregate(

            income=Sum("income"),

            expense=Sum("expense"),

        )

        income = finance["income"] or 0
        expense = finance["expense"] or 0

        return {
            "income": DashboardService.money(income),
            "expense": DashboardService.money(expense),
            "profit": DashboardService.money(income - expense),
        }
    @staticmethod
    def maintenance():

        maintenance = MaintenanceItem.objects.aggregate(

            repair_count=Count("id"),

            repair_cost=Sum("total_with_vat"),

        )

        return {

            "repair_count": maintenance["repair_count"] or 0,

            "repair_cost": float(maintenance["repair_cost"] or 0),

        }

    @staticmethod
    def top_regions():
        return list(

            ATMTURON.objects

            .values("region")

            .annotate(

                total=Count("id"),

                active=Count(
                    "id",
                    filter=Q(is_active=True),
                ),

                inactive=Count(
                    "id",
                    filter=Q(is_active=False),
                ),

                soz=Count(
                    "id",
                    filter=Q(
                        technical__status="SOZ"
                    ),
                ),

                nosoz=Count(
                    "id",
                    filter=Q(
                        technical__status="NOSOZ"
                    ),
                ),

                uzcard=Count(
                    "id",
                    filter=Q(
                        technical__card_type="UZCARD"
                    ),
                ),

                humo=Count(
                    "id",
                    filter=Q(
                        technical__card_type="HUMO"
                    ),
                ),

            )

            .order_by("-total")
        )

    @classmethod
    def dashboard(cls):
        return {
            "summary": cls.summary(),

            "finance": cls.finance(),

            "maintenance": cls.maintenance(),

            "top_regions": cls.top_regions(),

            "status_chart": DashboardChartService.status_chart(),

            "card_chart": DashboardChartService.card_chart(),

            "monthly_chart": DashboardChartService.monthly_chart(),

            "region_finance": DashboardChartService.region_finance(),

            "top_models": DashboardChartService.top_models(),

            "repair_trend": DashboardChartService.repair_trend(),
            "recent_maintenance": (
                DashboardChartService.recent_maintenance()
            ),
        }