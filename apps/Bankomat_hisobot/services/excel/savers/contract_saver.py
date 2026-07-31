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
            print("TOPILMADI:", parsed.terminal_id)
            return None

        contract, _ = ATMServiceContract.objects.get_or_create(
            atm=atm
        )

        return contract