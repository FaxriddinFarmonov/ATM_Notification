from django.db.models import Prefetch

from ..models.ATMServiceContract import ATMServicePayment
from ..models.ATMMonthlyStatistic import (
    ATMTURON,
    ATMMonthlyStatistic,
    ATMYearStatistic,
)


from django.db.models import Prefetch, Q

class ATMDetailQuerySet:

    @staticmethod
    def get(value):
        queryset = (
            ATMTURON.objects
            .select_related(
                "technical",
                "service_contract",
            )
            .prefetch_related(
                Prefetch(
                    "monthly_statistics",
                    queryset=ATMMonthlyStatistic.objects.order_by("-year", "-month"),
                ),
                Prefetch(
                    "year_statistics",
                    queryset=ATMYearStatistic.objects.order_by("-year"),
                ),
                Prefetch(
                    "service_contract__payments",
                    queryset=ATMServicePayment.objects.order_by("-year", "-month"),
                ),
                "technical__maintenance_items",
            )
        )

        if str(value).isdigit():
            try:
                return queryset.get(pk=int(value))
            except ATMTURON.DoesNotExist:
                return queryset.get(terminal_id=str(value))

        return queryset.get(terminal_id=str(value))