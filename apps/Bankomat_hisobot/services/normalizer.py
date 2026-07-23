import re


class HeaderNormalizer:

    @staticmethod
    def normalize(value):

        value = str(value)

        value = value.strip()

        value = value.lower()

        value = re.sub(r"\s+", " ", value)

        return value
HEADER_ALIASES = {

    "terminal id": "terminal_id",

    "terminal": "terminal_id",

    "merchant": "merchant_id",

    "merchand": "merchant_id",

    "merchant id": "merchant_id",

    "bxm yoki bxo nomi": "branch",

    "bxm": "branch",

    "bxo": "branch",

    "mfo": "mfo",

    "humo/uzcard": "card_type",

    "card": "card_type",

}