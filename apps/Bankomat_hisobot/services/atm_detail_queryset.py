from django.db.models import Prefetch

from ..models.ATMServiceContract import ATMServicePayment
from ..models.ATMMonthlyStatistic import (
    ATMTURON,
    ATMMonthlyStatistic,
    ATMYearStatistic,
)



class ATMDetailQuerySet:

    @staticmethod
    def get(pk):

        return (
            ATMTURON.objects
            .select_related(
                "technical",
                "service_contract",
            )
            .prefetch_related(
                Prefetch(
                    "monthly_statistics",
                    queryset=(
                        ATMMonthlyStatistic.objects
                        .order_by("-year", "-month")
                    ),
                ),
                Prefetch(
                    "year_statistics",
                    queryset=(
                        ATMYearStatistic.objects
                        .order_by("-year")
                    ),
                ),

                
                Prefetch(
                    "service_contract__payments",
                    queryset=(
                        ATMServicePayment.objects
                        .order_by(
                            "-year",
                            "-month",
                        )
                    ),
                ),
                "technical__maintenance_items",
            )
            .get(pk=pk)
        )