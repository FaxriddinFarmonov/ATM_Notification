from django.core.management.base import BaseCommand

from apps.atms.services.sync_service import SyncService


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        SyncService().run()

        self.stdout.write(
            self.style.SUCCESS(
                "Sync completed"
            )
        )