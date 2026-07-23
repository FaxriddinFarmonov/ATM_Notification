from apps.Bankomat_hisobot.models import (
    ATMServicePayment,
)


class PaymentSaver:

    @classmethod
    def save_services(
        cls,
        contract,
        parsed,
    ):

        for service in parsed.services:

            if service.service == "BTECH":

                contract.btech_monthly_fee = service.amount

            elif service.service == "GLOB":

                contract.glob_monthly_fee = service.amount

            elif service.service == "RENT":

                ATMServicePayment.objects.update_or_create(

                    contract=contract,

                    year=2026,

                    month=1,

                    payment_type="RENT",

                    defaults={

                        "amount": service.amount

                    }

                )

            elif service.service == "ELECTRICITY":

                ATMServicePayment.objects.update_or_create(

                    contract=contract,

                    year=2026,

                    month=1,

                    payment_type="ELECTRICITY",

                    defaults={

                        "amount": service.amount

                    }

                )

        contract.save()
    @classmethod
    def save_payments(
        cls,
        contract,
        parsed,
    ):

        for payment in parsed.payments:

            ATMServicePayment.objects.update_or_create(

                contract=contract,

                year=payment.year,

                month=payment.month,

                payment_type=payment.service,

                defaults={

                    "amount": payment.amount

                }

            )