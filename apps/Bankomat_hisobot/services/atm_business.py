from collections import defaultdict
from collections import defaultdict

from django.db.models import Sum
from django.db.models import Sum

from apps.maintenance.models import MaintenanceItem

class ATMBusinessService:

    def __init__(self, atm):

        self.atm = atm

        self.technical = getattr(
            atm,
            "technical",
            None,
        )

    def general(self):
        return {

            "region": self.atm.region,

            "name": self.atm.name,

            "address": self.atm.address,

            "card_type": self.atm.card_type,

            "model": self.atm.model,

        }

    def technical_information(self):
        if not self.technical:
            return {}

        return {

            "merchant_id": self.technical.merchant_id,

            "terminal_id": self.technical.terminal_id,

            "status": self.technical.status,

            "serial_number": self.technical.serial_number,

            "inventory_number": self.technical.inventory_number,

            "account_23510": self.technical.account_23510,

            "account_45265": self.technical.account_45265,

        }

    from collections import defaultdict
    from django.db.models import Sum

    def _maintenance_cache(self):

        cache = defaultdict(
            lambda: {
                "repair_cost": 0,
                "quantity": 0,
            }
        )

        if not self.technical:
            return cache

        statistics = (

            self.technical

            .maintenance_items

            .values(
                "protocol_date__year",
                "protocol_date__month",
            )

            .annotate(
                repair_cost=Sum("total_with_vat"),
                quantity=Sum("quantity"),
            )

        )

        for row in statistics:
            cache[
                (
                    row["protocol_date__year"],
                    row["protocol_date__month"],
                )
            ] = {

                "repair_cost": row["repair_cost"] or 0,

                "quantity": row["quantity"] or 0,

            }

        return cache

    def monthly_statistics(self):

        cache = self._maintenance_cache()

        result = []

        for item in self.atm.monthly_statistics.all():
            maintenance = cache.get(
                (
                    item.year,
                    item.month,
                ),
                {
                    "repair_cost": 0,
                    "quantity": 0,
                },
            )

            result.append(

                {

                    "year": item.year,

                    "month": item.month,

                    "income": item.income,

                    "expense": item.expense,

                    "repair_cost": maintenance["repair_cost"],

                    "quantity": maintenance["quantity"],

                }

            )

        return result

    def build(self):

        return {

            "general": self.general(),

            "technical": self.technical_information(),

            "service_contract": self.service_contract(),

            "monthly_statistics": self.monthly_statistics(),

            "yearly_statistics": self.yearly_statistics(),

        }

    def _maintenance_year_cache(self):

        cache = defaultdict(
            lambda: {
                "repair_cost": 0,
                "quantity": 0,
            }
        )

        if not self.technical:
            return cache

        statistics = (

            self.technical

            .maintenance_items

            .values(
                "protocol_date__year",
            )

            .annotate(

                repair_cost=Sum("total_with_vat"),

                quantity=Sum("quantity"),

            )

        )

        for row in statistics:
            cache[
                row["protocol_date__year"]
            ] = {

                "repair_cost": row["repair_cost"] or 0,

                "quantity": row["quantity"] or 0,

            }

        return cache

    def yearly_statistics(self):

        cache = self._maintenance_year_cache()

        result = []

        for item in self.atm.year_statistics.all():
            maintenance = cache.get(

                item.year,

                {

                    "repair_cost": 0,

                    "quantity": 0,

                },

            )

            result.append(

                {

                    "year": item.year,

                    "card_type": item.card_type,

                    "income": item.income,

                    "expense": item.expense,

                    "repair_cost": maintenance["repair_cost"],

                    "quantity": maintenance["quantity"],

                }

            )

        return result

    def service_contract(self):

        contract = getattr(
            self.atm,
            "service_contract",
            None,
        )

        if not contract:
            return None

        return {

            "btech_monthly_fee": contract.btech_monthly_fee,

            "glob_monthly_fee": contract.glob_monthly_fee,

            "payments": [

                {

                    "year": payment.year,

                    "month": payment.month,

                    "payment_type": payment.payment_type,

                    "amount": payment.amount,

                }

                for payment in contract.payments.all()

            ],

        }