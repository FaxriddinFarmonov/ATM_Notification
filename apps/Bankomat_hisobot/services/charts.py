from django.db.models import Count, Sum, Q
from django.db.models.functions import Coalesce
from apps.maintenance.models import MaintenanceItem
from apps.Bankomat_hisobot.models.ATMMonthlyStatistic import (
    ATMTURON,
    ATMMonthlyStatistic
)
from django.db.models.functions import (
    ExtractYear,
    ExtractMonth,
)

class DashboardChartService:

    @staticmethod
    def status_chart():
        queryset = (
            ATMTURON.objects
            .values("technical__status")
            .annotate(
                value=Count("id")
            )
            .order_by("technical__status")
        )

        result = [
            {
                "name": item["technical__status"],
                "value": item["value"],
            }
            for item in queryset
        ]


        return result

    @staticmethod
    def card_chart():
        queryset = (
            ATMTURON.objects
            .values("technical__card_type")
            .annotate(
                value=Count("id")
            )
            .order_by("technical__card_type")
        )

        result = [
            {
                "name": item["technical__card_type"],
                "value": item["value"],
            }
            for item in queryset
        ]
        return result

    @staticmethod
    def monthly_chart():

        queryset = (
            ATMMonthlyStatistic.objects
            .values(
                "year",
                "month",
            )
            .annotate(
                income=Sum("income"),
                expense=Sum("expense"),
            )
            .order_by(
                "year",
                "month",
            )
        )

        return [
            {
                "year": item["year"],
                "month": item["month"],
                "income": item["income"] or 0,
                "expense": item["expense"] or 0,
                "profit": (
                    item["income"] or 0
                ) - (
                    item["expense"] or 0
                ),
            }
            for item in queryset
        ]

    @staticmethod
    def region_finance():

        queryset = (
            ATMMonthlyStatistic.objects
            .values(
                "atm__region",
            )
            .annotate(
                income=Sum("income"),
                expense=Sum("expense"),
            )
            .order_by(
                "-income",
            )
        )

        return [
            {
                "region": item["atm__region"],
                "income": item["income"] or 0,
                "expense": item["expense"] or 0,
                "profit": (
                    item["income"] or 0
                ) - (
                    item["expense"] or 0
                ),
            }
            for item in queryset
        ]

    @staticmethod
    def top_models():

        queryset = (
            ATMTURON.objects
            .values(
                "model",
            )
            .annotate(
                total=Count("id"),

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
            )
            .order_by(
                "-total",
                "model",
            )
        )

        return [
            {
                "model": item["model"],
                "total": item["total"],
                "soz": item["soz"],
                "nosoz": item["nosoz"],
            }
            for item in queryset
        ]
    @staticmethod
    def repair_trend():

        queryset = (
            MaintenanceItem.objects
            .filter(
                protocol_date__isnull=False
            )
            .annotate(
                year=ExtractYear("protocol_date"),
                month=ExtractMonth("protocol_date"),
            )
            .values(
                "year",
                "month",
            )
            .annotate(
                repair_count=Count("id"),
                repair_cost=Sum("total_amount"),
            )
            .order_by(
                "year",
                "month",
            )
        )

        return [
            {
                "year": item["year"],
                "month": item["month"],
                "repair_count": item["repair_count"],
                "repair_cost": item["repair_cost"] or 0,
            }
            for item in queryset
        ]

    @staticmethod
    def recent_maintenance(limit=10):

        queryset = (
            MaintenanceItem.objects
            .select_related(
                "technical",
                "technical__atm",
                "protocol",
            )
            .only(
                "id",
                "protocol_date",
                "part_name",
                "quantity",
                "total_amount",
                "technical__serial_number",
                "technical__terminal_id",
                "technical__atm__region",
                "protocol__protocol_number",
            )
            .order_by(
                "-protocol_date",
                "-id",
            )[:limit]
        )

        return [
            {
                "id": item.id,
                "protocol_number": (
                    item.protocol.protocol_number
                    if item.protocol
                    else None
                ),
                "protocol_date": item.protocol_date,
                "part_name": item.part_name,
                "quantity": item.quantity,
                "total_amount": item.total_amount,
                "atm": {
                    "terminal_id": (
                        item.technical.terminal_id
                        if item.technical
                        else None
                    ),
                    "serial_number": (
                        item.technical.serial_number
                        if item.technical
                        else None
                    ),
                    "region": (
                        item.technical.atm.region
                        if item.technical
                        and item.technical.atm
                        else None
                    ),
                },
            }
            for item in queryset
        ]