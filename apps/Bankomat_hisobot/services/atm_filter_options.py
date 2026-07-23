from apps.Bankomat_hisobot.models import (
    ATMTURON,
    ATMTechnical,
    ATMYearStatistic,
)


class ATMFilterOptionsService:

    @staticmethod
    def get():

        return {

            "status": ATMFilterOptionsService.status(),

            "card_type": ATMFilterOptionsService.card_types(),

            "regions": ATMFilterOptionsService.regions(),

            "models": ATMFilterOptionsService.models(),

            "model_names": ATMFilterOptionsService.model_names(),

            "years": ATMFilterOptionsService.years(),

            "months": ATMFilterOptionsService.months(),

            "is_active": ATMFilterOptionsService.is_active(),

        }

    @staticmethod
    def status():

        return [

            {
                "value": value,
                "label": label,
            }

            for value, label
            in ATMTechnical.STATUS_CHOICES

        ]

    @staticmethod
    def card_types():

        return [

            {
                "value": value,
                "label": label,
            }

            for value, label
            in ATMTechnical.CARD_CHOICES

        ]

    @staticmethod
    def regions():

        return list(

            ATMTURON.objects

            .exclude(region="")

            .values_list(
                "region",
                flat=True,
            )

            .distinct()

            .order_by("region")

        )

    @staticmethod
    def models():

        return list(

            ATMTURON.objects

            .exclude(model="")

            .values_list(
                "model",
                flat=True,
            )

            .distinct()

            .order_by("model")

        )

    @staticmethod
    def model_names():

        return list(

            ATMTechnical.objects

            .exclude(model_name="")

            .values_list(
                "model_name",
                flat=True,
            )

            .distinct()

            .order_by("model_name")

        )

    @staticmethod
    def years():

        return list(

            ATMYearStatistic.objects

            .values_list(
                "year",
                flat=True,
            )

            .distinct()

            .order_by("-year")

        )

    @staticmethod
    def months():

        return [

            {
                "value": 1,
                "label": "Yanvar",
            },
            {
                "value": 2,
                "label": "Fevral",
            },
            {
                "value": 3,
                "label": "Mart",
            },
            {
                "value": 4,
                "label": "Aprel",
            },
            {
                "value": 5,
                "label": "May",
            },
            {
                "value": 6,
                "label": "Iyun",
            },
            {
                "value": 7,
                "label": "Iyul",
            },
            {
                "value": 8,
                "label": "Avgust",
            },
            {
                "value": 9,
                "label": "Sentabr",
            },
            {
                "value": 10,
                "label": "Oktabr",
            },
            {
                "value": 11,
                "label": "Noyabr",
            },
            {
                "value": 12,
                "label": "Dekabr",
            },

        ]

    @staticmethod
    def is_active():

        return [

            {
                "value": True,
                "label": "Faol",
            },

            {
                "value": False,
                "label": "Faol emas",
            },

        ]