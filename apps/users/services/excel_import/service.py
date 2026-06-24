# service.py

from django.db import transaction

from apps.users.models import Engineer
from apps.atms.models import ATM

from .reader import ExcelReader
from .normalizer import ExcelNormalizer
from .matcher import ATMSmartMatcher


class ExcelImportService:

    def __init__(self, path):
        self.path = path
        self.reader = ExcelReader()
        self.normalizer = ExcelNormalizer()
        self.matcher = ATMSmartMatcher()

    @transaction.atomic
    def run(self):

        rows = self.reader.read(self.path)

        matched = 0
        created_engineers = 0

        for row in rows:

            data = self.normalizer.normalize(row)

            engineer, created = Engineer.objects.get_or_create(
                telegram_chat_id=data["telegram_chat_id"],
                defaults={
                    "full_name": data["fio"],
                    "phone": data["phone"],
                }
            )

            if created:
                created_engineers += 1

            atm = self.matcher.find(data)

            if atm:
                atm.responsible_engineer = engineer
                atm.save(update_fields=["responsible_engineer"])
                matched += 1

        print(f"Matched ATMs: {matched}")
        print(f"New Engineers: {created_engineers}")