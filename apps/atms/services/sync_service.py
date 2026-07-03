
from django.db import transaction
from .monitoring_client import MonitoringClient
from .event_engine import EventEngine
from apps.atms.models import ATM, ATMCurrentState

class SyncService:

    def run(self):
        client = MonitoringClient()
        data = client.get_atms()

        print("ATM COUNT:", len(data))

        self.sync_atms(data)

    @transaction.atomic
    def sync_atms(self, data):

        for item in data:

            atm, _ = ATM.objects.update_or_create(
                external_id=item["id"],
                defaults={
                    "atm_uid": item.get("atmUid"),
                    "serial": item.get("serial"),
                    "tid": item.get("tid"),
                    "branch_number": item.get("card", {}).get("branchNumber"),
                    "address": item.get("card", {}).get("address"),
                    "model_name": item.get("model", {}).get("name"),
                    "extra_attrs": item.get("card", {}).get("extraAttrs", {})
                }
            )

            # ⚡ FAST STATE READ (NO SERIALIZATION)
            old_state = ATMCurrentState.objects.filter(
                atm_id=atm.id
            ).values(
                "agent_status",
                "cash_amount"
            ).first() or {}

            # 1. sync state
            self.sync_current_state(atm, item)

            # 2. sync cassettes (fast version)

            # 3. event engine (ONLY ONCE)
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

