
from apps.atms.models import ATMEvent

from datetime import timedelta
from django.utils import timezone


class EventEngine:

    CASH_THRESHOLD = 50_000_000
    TX_LIMIT_HOURS = 15

    def __init__(self, atm, item, old_state):
        self.atm = atm
        self.item = item
        self.old = old_state

    def run(self):

        self.check_cash_low()
        self.check_no_transaction()

    # ------------------------
    # 💰 CASH LOW RULE
    # ------------------------
    def check_cash_low(self):

        remaining = int(
            (self.item.get("cdmRemainingAmount") or {}).get("totalUzs") or 0
        )

        if remaining >= self.CASH_THRESHOLD:
            return

        last_event = self._last_event("BANKOMATDA_PUL_KAM")

        # 🔥 30 minut ichida qayta yubormaslik
        if last_event and (timezone.now() - last_event.created_at).seconds < 1800:
            return

        self._create_event(
            "BANKOMATDA_PUL_KAM",
            f"Bankomatda pul kam: {remaining:,} UZS"
        )
    # ------------------------
    def check_no_transaction(self):

        tx = self.item.get("lastTransactionTimestamp") or {}
        cash_out = tx.get("cashOut") if isinstance(tx, dict) else None

        if not cash_out:
            return

        try:
            last_time = timezone.datetime.fromisoformat(
                cash_out.replace("Z", "+00:00")
            )

            diff = timezone.now() - last_time

            if diff < timedelta(hours=self.TX_LIMIT_HOURS):
                return

            last_event = self._last_event("TRANZAKSIYA_YO'Q")

            if last_event and (timezone.now() - last_event.created_at).seconds < 1800:
                return

         
            hours = int(diff.total_seconds() // 3600)

            self._create_event(
           	 "TRANZAKSIYA_YO'Q",
   	   	 f"{hours} soatdan beri tranzaksiya yo‘q")
        except Exception:
            return

    # ------------------------
    def _create_event(self, event_type, message):

        def _last_event(self, event_type):
            return ATMEvent.objects.filter(
                atm=self.atm,
                event_type=event_type
            ).order_by("-id").first()



        ATMEvent.objects.create(
            atm=self.atm,
            event_type=event_type,
            message=message
        )

    def _last_event(self, event_type):
        return ATMEvent.objects.filter(
            atm=self.atm,
            event_type=event_type
        ).order_by("-created_at").first()
