from apps.Bankomat_hisobot.models.ATMMonthlyStatistic import (
    ATMTURON,
)


class DatabaseContextService:

    @staticmethod
    def get_context() -> dict:

        regions = list(
            ATMTURON.objects
            .exclude(region__isnull=True)
            .exclude(region="")
            .values_list(
                "region",
                flat=True,
            )
            .distinct()
            .order_by("region")
        )

        models = list(
            ATMTURON.objects
            .exclude(model__isnull=True)
            .exclude(model="")
            .values_list(
                "model",
                flat=True,
            )
            .distinct()
            .order_by("model")
        )

        card_types = list(
            ATMTURON.objects
            .exclude(card_type__isnull=True)
            .exclude(card_type="")
            .values_list(
                "card_type",
                flat=True,
            )
            .distinct()
            .order_by("card_type")
        )

        return {
            "regions": regions,
            "models": models,
            "card_types": card_types,
            "statuses": [
                "SOZ",
                "NOSOZ",
            ],
        }