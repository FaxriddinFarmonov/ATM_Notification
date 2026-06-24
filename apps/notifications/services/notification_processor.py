from apps.notifications.models import Notification
from .telegram_sender import TelegramSender

from .routing_engine import RoutingEngine

class NotificationProcessor:

    def run(self):

        notifications = Notification.objects.filter(status="PENDING")

        for n in notifications:

            success = TelegramSender.send_message(
                chat_id=n.chat_id,
                text=n.text
            )

            if success:
                n.status = "SENT"
            else:
                n.status = "FAILED"
                n.retry_count += 1

            n.save()