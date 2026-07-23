from dataclasses import dataclass, field
from decimal import Decimal



@dataclass(slots=True)
class ParsedService:

    service: str

    amount: Decimal


@dataclass(slots=True)
class ParsedPayment:

    service: str

    year: int

    month: int

    amount: Decimal


@dataclass(slots=True)
class ParsedRow:

    terminal_id: str

    merchant_id: str

    branch: str

    mfo: str

    card_type: str

    services: list[ParsedService] = field(
        default_factory=list
    )

    payments: list[ParsedPayment] = field(
        default_factory=list
    )

    def has_services(self):

        return bool(self.services)

    def has_payments(self):

        return bool(self.payments)

    def is_valid(self):

        return bool(
            self.terminal_id
        )

    @property
    def service_count(self):

        return len(
            self.services
        )

    @property
    def payment_count(self):

        return len(
            self.payments
        )