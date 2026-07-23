import re

from .months import MONTHS
from .normalizer import HeaderNormalizer


class HeaderAnalyzer:
    MONTH_PATTERN = re.compile(

        r"(?P<year>\d{4})\s+(?P<month>.+)",

        re.IGNORECASE,

    )

    @classmethod
    def analyze(cls, headers):

        schema = []

        for index, header in enumerate(headers):

            item = cls.parse(index, header)

            if item:
                schema.append(item)

        return schema