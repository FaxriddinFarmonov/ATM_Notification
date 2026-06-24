from django.core.management.base import BaseCommand
from apps.users.services.excel_import.service import ExcelImportService


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("path", type=str)

    def handle(self, *args, **kwargs):

        path = kwargs["path"]

        service = ExcelImportService(path)
        service.run()

        self.stdout.write(self.style.SUCCESS("Excel import done"))