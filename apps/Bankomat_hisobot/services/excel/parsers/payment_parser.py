from decimal import Decimal

from ..parsed_row import ParsedPayment
from decimal import Decimal, InvalidOperation

from ..parsed_row import ParsedPayment


class PaymentParser:

    @staticmethod
    def parse_amount(value):

        if value is None:
            return None

        text = str(value).strip()

        if not text:
            return None

        if text in {
            "-",
            "--",
            "---",
        }:
            return None

        # 1 848  -> 1848
        text = text.replace(" ", "")

        # 1128,7 -> 1128.7
        text = text.replace(",", ".")

        try:
            return Decimal(text)

        except InvalidOperation:

            raise ValueError(
                f"To'lov summasi noto'g'ri: {value!r}"
            )

    @classmethod
    def apply(
        cls,
        row,
        column,
        value,
    ):

        amount = cls.parse_amount(value)

        if amount is None:
            return

        row.payments.append(
            ParsedPayment(
                service=column.service,
                year=column.year,
                month=column.month,
                amount=amount,
            )
        )