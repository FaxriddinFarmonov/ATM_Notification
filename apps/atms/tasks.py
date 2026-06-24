from celery import shared_task

from apps.atms.models import ATMEvent
from apps.atms.services.sync_service import SyncService



@shared_task
def sync_atms():

    # eski eventlarni tozalash
    ATMEvent.objects.all().delete()

    # yangi snapshot olish
    SyncService().run()