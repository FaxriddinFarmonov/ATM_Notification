# faxriddin
from django.db import transaction
from .monitoring_client import MonitoringClient
from .event_engine import EventEngine
from apps.atms.models  import ATM, ATMCurrentState

class SyncService:

    def run(self):
        client = MonitoringClient()
        data = client.get_atms()

        print("ATM COUNT:", len(data))

        self.sync_atms(data)

    @transaction.atomic
    def sync_atms(self, data):

        for item in data:
            card = item.get("card", {})
            extra = card.get("extraAttrs", {})

            atm, _ = ATM.objects.update_or_create(
                external_id=item["id"],
                defaults={
                    "atm_uid": item.get("atmUid"),
                    "serial": item.get("serial"),

                    # Terminal ID ni saqlaymiz
                    "tid": extra.get("terminalId"),

                    "branch_number": card.get("branchNumber"),
                    "address": card.get("address"),
                    "model_name": item.get("model", {}).get("name"),
                    "extra_attrs": extra,
                }
            )

            # ⚡ FAST STATE READ (NO SERIALIZATION)
            old_state = (
                    ATMCurrentState.objects.filter(atm_id=atm.id)
                    .values(
                        "agent_status",
                        "cash_amount",
                    )
                    .first()
                    or {}
            )

            # 1. Sync current state
            self.sync_current_state(atm, item)

            # 2. Event engine
            EventEngine(atm, item, old_state).run()

    def sync_current_state(self, atm, item):
        ATMCurrentState.objects.update_or_create(
            atm=atm,
            defaults={
                "agent_status": item.get("agentStatus", {}).get("status", "UNKNOWN"),
                "service_status": item.get("state", {}).get("serviceStatus", "UNKNOWN"),
                "app_status": item.get("state", {}).get("appStatus", "UNKNOWN"),
                "app_conn_status": item.get("state", {}).get("appConnStatus", "UNKNOWN"),
                "cash_amount": self.get_cash_amount(item),
                "last_online": item.get("agentStatus", {}).get("lastOnline"),
            }
        )

    def get_cash_amount(self, item):
        try:
            return int(item.get("cdmRemainingAmount", {}).get("totalUzs") or 0)
        except:
            return 0

