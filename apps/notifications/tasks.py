from celery import shared_task
from apps.notifications.services.send_notifications import SendNotificationService
from celery import shared_task
from .services.notification_generator import NotificationGenerator
from celery import shared_task
from django.core.cache import cache

from .services.notification_generator import NotificationGenerator
from .services.send_notifications import SendNotificationService


def locked(key, timeout=60):
    if cache.get(key):
        return False

    cache.set(key, True, timeout=timeout)
    return True


@shared_task
def generate_notifications():

    if not locked("generate_notifications_lock"):
        return

    NotificationGenerator().run()


@shared_task
def send_notifications():

    if not locked("send_notifications_lock"):
        return

    SendNotificationService().run()