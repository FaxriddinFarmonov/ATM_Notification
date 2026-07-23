from django.core.management.base import BaseCommand

from apps.Bankomat_hisobot.models.ATMServiceContract import (
    ATMServiceType,
)


DEFAULT_TYPES = [

    ("btech", "BTECH"),

    ("glob", "GLOB"),

    ("incassation", "Inkassatsiya"),

    ("rent", "Arenda"),

    ("electricity", "Elektr"),

]


class Command(BaseCommand):

    help = "Create default ATM service types."

    def handle(self, *args, **options):

        for code, name in DEFAULT_TYPES:

            ATMServiceType.objects.get_or_create(

                code=code,

                defaults={

                    "name": name,

                }

            )

        self.stdout.write(

            self.style.SUCCESS(

                "ATM service types created."

            )

        )