from django.db.models import Prefetch

from ..models.ATMMonthlyStatistic import (
    ATMTURON,
    ATMMonthlyStatistic,
)

from apps.maintenance.models import MaintenanceItem
from django.db.models import (
    OuterRef,
    Subquery,
    Count,
    DateField,
    DecimalField,
)

class ATMQuerySet:

    @staticmethod
    def list():

        return (
            ATMTURON.objects
            .filter(is_active=True)

            .select_related("technical")

            .only(
                "id",
                "name",
                "region",

                "technical__terminal_id",
                "technical__merchant_id",
                "technical__serial_number",
                "technical__status",
                "technical__card_type",
                "technical__model_name",
                "technical__address",
            )
        )

    @staticmethod
    def _last_monthly():
        return (
            ATMMonthlyStatistic.objects
            .filter(
                atm=OuterRef("pk")
            )
            .order_by(
                "-year",
                "-month",
            )
        )