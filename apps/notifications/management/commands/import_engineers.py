# management/commands/import_engineers.py

from django.core.management.base import BaseCommand
from apps.users.services.excel_import.service import ExcelImportService


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("path", type=str)

    def handle(self, *args, **kwargs):

        ExcelImportService(kwargs["path"]).run()

        self.stdout.write(self.style.SUCCESS("Import completed"))