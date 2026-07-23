from decimal import Decimal

from ..parsed_row import ParsedService


class ServiceParser:

    @classmethod
    def apply(
        cls,
        row,
        column,
        value,
    ):

        if value in (None, ""):
            return

        row.services.append(
            ParsedService(
                service=column.service,
                amount=Decimal(str(value)),
            )
        )