
from django.db import transaction
from apps.atms.models import ATMEvent
from apps.notifications.models import Notification
from .routing_engine import RoutingEngine
from .event_message_builder import EventMessageBuilder


class NotificationGenerator:

    def run(self):

        events = ATMEvent.objects.filter(
            is_sent=False
        ).select_related("atm")

        routing = RoutingEngine()

        for event in events:

            message = EventMessageBuilder.build(event)

            if not message:
                continue

            recipients = routing.get_recipients(event.atm)

            for chat_id in recipients:

                Notification.objects.create(
                    event=event,
                    chat_id=str(chat_id),   # 🔥 IMPORTANT FIX
                    text=message,
                    status="PENDING"
                )

            # ❌ NO SAFE FILTER, NO CHECK, DIRECT MARK
            event.is_sent = True
            event.save(update_fields=["is_sent"])