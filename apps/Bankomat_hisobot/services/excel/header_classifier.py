import re

from .schema import ColumnSchema


class HeaderClassifier:

    STATIC_FIELDS = {

        "bxm yoki bxo nomi": "branch",

        "mfo": "mfo",

        "humo/uzcard": "card_type",

        "terminal id": "terminal_id",

        "merchand": "merchant_id",

    }

    SERVICE_HEADERS = {

        "btech serviz tashkilotiga oylik tulov": "BTECH",

        "glob serviz tashkilotiga oylik tulov": "GLOB",

        "inkasatsiya shartnomasi boyicha oylik tolovi": "INCASSATION",

        "arenda tulovi": "RENT",

        "elektrenergo": "ELECTRICITY",

    }

    MONTHS = {

        "yanvar": 1,

        "fevral": 2,

        "mart": 3,

        "aprel": 4,

        "may": 5,

        "iyun": 6,
        "июн": 6,

        "iyul": 7,
        "июл": 7,

        "avgust": 8,
        "август": 8,

        "sentabr": 9,
        "сентябрь": 9,

        "oktabr": 10,
        "октябрь": 10,

        "noyabr": 11,
        "ноябрь": 11,

        "dekabr": 12,
        "декабрь": 12,

    }

    @classmethod
    def classify(
        cls,
        index,
        header,
    ):

        left, *right = header.split("|")

        left = left.strip().lower()

        right = right[0].strip().lower() if right else ""

        if left in cls.STATIC_FIELDS:

            return ColumnSchema(

                index=index,

                header=header,

                category="static",

                field=cls.STATIC_FIELDS[left],

            )

        if left in cls.SERVICE_HEADERS:

            service = cls.SERVICE_HEADERS[left]

            year = None
            month = None

            match = re.search(
                r"\d{4}",
                right,
            )

            if match:

                year = int(match.group())

            for month_name, month_number in cls.MONTHS.items():

                if month_name in right:

                    month = month_number

                    break

            return ColumnSchema(

                index=index,

                header=header,

                category="payment" if month else "service",

                service=service,

                year=year,

                month=month,

            )

        return ColumnSchema(

            index=index,

            header=header,

            category="ignore",

        )