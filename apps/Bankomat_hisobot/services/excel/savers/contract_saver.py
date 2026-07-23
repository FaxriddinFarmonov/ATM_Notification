from apps.Bankomat_hisobot.models import (
    ATMTURON,
    ATMServiceContract,
)


class ContractSaver:

    @classmethod
    def save(cls, parsed):
        atm = (
            ATMTURON.objects
            .filter(
                terminal_id=str(parsed.terminal_id).strip()
            )
            .first()
        )

        if atm is None:
            print(
                "TOPILMADI:",
                parsed.terminal_id,
            )

            return None
        contract, _ = ATMServiceContract.objects.update_or_create(

            atm=atm,

            defaults={

                "bxm_name": parsed.branch,

                "mfo": parsed.mfo,

                "merchant_id": parsed.merchant_id,

                "card_type": parsed.card_type,

            }

        )

        return contract