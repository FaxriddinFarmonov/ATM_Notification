from django.core.management.base import BaseCommand
from apps.notifications.services.notification_processor import NotificationProcessor

from django.utils import timezone
from apps.notifications.models import Notification
from .telegram_sender import TelegramSender



class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        NotificationProcessor().run()

        self.stdout.write("Notifications processed")



import time
from django.utils import timezone
from apps.notifications.models import Notification
from .telegram_sender import TelegramSender


class SendNotificationService:

    def run(self):

        notifications = Notification.objects.filter(
            status="PENDING"
        ).select_related("event")[:15]

        for n in notifications:

            ok = TelegramSender.send_message(
                chat_id=n.chat_id,
                text=n.text
            )

            if ok:
                n.status = "SENT"
                n.sent_at = timezone.now()
            else:
                # FAILED qilmaymiz
                n.status = "PENDING"

            n.save(update_fields=["status", "sent_at"])

            # Telegramni bo'g'maslik uchun
            time.sleep(1)