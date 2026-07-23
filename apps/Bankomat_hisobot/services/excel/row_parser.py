from decimal import Decimal
from .parsers.static_parser import StaticParser
from .parsers.service_parser import ServiceParser
from .parsers.payment_parser import PaymentParser
from .parsed_row import (
    ParsedRow,
    ParsedService,
    ParsedPayment,
)


class RowParser:

    @classmethod
    def parse(
        cls,
        schema,
        values,
    ):

        row = ParsedRow(

            terminal_id="",

            merchant_id="",

            branch="",

            mfo="",

            card_type="",

        )

        for column in schema:

            value = values[
                column.index
            ]

            cls._apply(
                row=row,
                column=column,
                value=value,
            )

        return row

    @classmethod
    def _apply(
            cls,
            row,
            column,
            value,
    ):

        if column.category == "static":

            StaticParser.apply(
                row=row,
                column=column,
                value=value,
            )

        elif column.category == "service":

            ServiceParser.apply(
                row=row,
                column=column,
                value=value,
            )

        elif column.category == "payment":

            PaymentParser.apply(
                row=row,
                column=column,
                value=value,
            )
