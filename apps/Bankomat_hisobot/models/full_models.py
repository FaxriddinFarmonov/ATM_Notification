from django.db import models

from .ATMMonthlyStatistic import ATMTURON


class ATMTechnical(models.Model):
    STATUS_CHOICES = (
        ("SOZ", "Soz"),
        ("NOSOZ", "Nosoz"),
    )

    CARD_CHOICES = (
        ("UZCARD", "Uzcard"),
        ("HUMO", "Humo"),
        ("VASH", "Vash"),
    )
    atm = models.OneToOneField(
        ATMTURON,
        on_delete=models.CASCADE,
        related_name="technical",
        null=True,
        blank=True,
    )

    card_type = models.CharField(
        max_length=20,
        choices=CARD_CHOICES,
        db_index=True
    )

    model_name = models.CharField(
        max_length=100,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        db_index=True
    )

    serial_number = models.CharField(
        max_length=100,
        blank=True,
        db_index=True
    )

    inventory_number = models.CharField(
        max_length=100,
        blank=True
    )

    address = models.TextField()

    merchant_id = models.CharField(
        max_length=100,
        blank=True
    )

    terminal_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True
    )

    account_23510 = models.CharField(
        max_length=100,
        blank=True
    )

    account_45265 = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ("terminal_id",)
        verbose_name = "ATM Technical"
        verbose_name_plural = "ATM Technicals"

    def __str__(self):
        return f"{self.terminal_id} ({self.card_type})"


class ATMImportFile(models.Model):

    file = models.FileField(
        upload_to="atm/imports/"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_processed = models.BooleanField(
        default=False
    )

    result = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.file.name