from celery import shared_task

from apps.atms.models import ATMEvent
from apps.atms.services.sync_service import SyncService



@shared_task
def sync_atms():

    # eski eventlarni tozalash
    ATMEvent.objects.all().delete()

    # yangi snapshot olish
    SyncService().run()


@shared_task
def sync_btech_atms_hourly():
    from apps.atms.services.btech_sync import BTechSyncService
    return BTechSyncService.sync_all()