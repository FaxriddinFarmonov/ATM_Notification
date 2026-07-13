# apps/atm/full_models.py

from django.db import models


class ATMTURON(models.Model):
    class CardType(models.TextChoices):
        UZCARD = "UZCARD", "Uzcard"
        HUMO = "HUMO", "Humo"

    region = models.CharField(
        max_length=100,
        verbose_name="Viloyat"
    )

    name = models.CharField(
        max_length=255,
        verbose_name="ATM nomi"
    )

    address = models.TextField(
        verbose_name="Manzil"
    )

    terminal_id = models.CharField(
        max_length=30,
        unique=False,
        db_index=True
    )

    model = models.CharField(
        max_length=100
    )

    card_type = models.CharField(
        max_length=20,
        choices=CardType.choices,
        db_index=True
    )

    is_active = models.BooleanField(
        default=True
    )

    note = models.TextField(
        blank=True,
        default=""
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["region", "terminal_id"]

    def __str__(self):
        return f"{self.terminal_id} - {self.address}"


class ATMMonthlyStatistic(models.Model):

    atm = models.ForeignKey(
        ATMTURON,
        on_delete=models.CASCADE,
        related_name="monthly_statistics"
    )

    year = models.PositiveSmallIntegerField()

    month = models.PositiveSmallIntegerField()

    expense = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        default=0
    )

    income = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "atm",
            "year",
            "month",
        )

        ordering = [
            "year",
            "month",
        ]

    def __str__(self):
        month_names = {
            1: "Yanvar",
            2: "Fevral",
            3: "Mart",
            4: "Aprel",
            5: "May",
            6: "Iyun",
            7: "Iyul",
            8: "Avgust",
            9: "Sentabr",
            10: "Oktabr",
            11: "Noyabr",
            12: "Dekabr",
        }

        return (
            f"{self.atm.terminal_id} | "
            f"{month_names.get(self.month, self.month)} "
            f"{self.year}"
        )



class ATMYearStatistic(models.Model):

    atm = models.ForeignKey(
        ATMTURON,
        on_delete=models.CASCADE,
        related_name="year_statistics"
    )

    year = models.PositiveSmallIntegerField()
    card_type = models.CharField(
        max_length=20,
        choices=[
            ("UZCARD", "Uzcard"),
            ("HUMO", "Humo"),
        ],
        db_index=True,
    )
    expense = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        default=0
    )

    income = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        default=0
    )

    class Meta:
        unique_together = (
            "atm",
            "year",
            "card_type",
        )

        ordering = [
            "year"
        ]

    def __str__(self):
        return (
            f"{self.atm.terminal_id} | "
            f"{self.year} | "
            f"{self.card_type}"
        )

class ExcelImport(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    file = models.FileField(
        upload_to="atm/imports/"
    )

    imported_rows = models.PositiveIntegerField(
        default=0
    )

    success = models.BooleanField(
        default=True
    )

    error = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.file.name


class ExcelImport(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    file = models.FileField(
        upload_to="atm/imports/"
    )

    imported_rows = models.PositiveIntegerField(
        default=0
    )

    success = models.BooleanField(
        default=True
    )

    error = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.file.name