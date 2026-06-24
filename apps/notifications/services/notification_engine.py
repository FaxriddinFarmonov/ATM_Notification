
from apps.notifications.models import Notification
from apps.notifications.services.message_builder import MessageBuilder
from .event_message_builder import EventMessageBuilder


class NotificationEngine:

    @staticmethod
    def create(event):

        engineer = event.atm.responsible_engineer

        if not engineer or not engineer.telegram_chat_id:
            return

        text = EventMessageBuilder.build(event)

        Notification.objects.create(
            event=event,
            chat_id=engineer.telegram_chat_id,
            text=text
        )