import uuid

from django.db import models


class BaseModel(models.Model):
    """
    Barcha modellar uchun umumiy model.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True



class Region(BaseModel):

    name = models.CharField(
        max_length=100,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Viloyat"
        verbose_name_plural = "Viloyatlar"

    def __str__(self):
        return self.name


class Branch(BaseModel):

    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="branches"
    )

    name = models.CharField(
        max_length=255
    )

    legal_address = models.TextField()

    class Meta:
        ordering = ["name"]
        unique_together = ("region", "name")

    def __str__(self):
        return f"{self.region.name} - {self.name}"

class ATMType(BaseModel):

    name = models.CharField(
        max_length=50,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ATMModel(BaseModel):

    manufacturer = models.CharField(
        max_length=100,
        blank=True
    )

    name = models.CharField(
        max_length=100,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ATMStatus(models.TextChoices):

    ACTIVE = "active", "Soz"

    INACTIVE = "inactive", "Nosoz"


class ATM(BaseModel):

    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name="atms"
    )

    atm_type = models.ForeignKey(
        ATMType,
        on_delete=models.PROTECT
    )

    atm_model = models.ForeignKey(
        ATMModel,
        on_delete=models.PROTECT
    )

    status = models.CharField(
        max_length=20,
        choices=ATMStatus.choices,
        default=ATMStatus.ACTIVE
    )

    serial_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_index=True,
    )

    inventory_number = models.CharField(
        max_length=100,
        db_index=True
    )

    merchant_id = models.CharField(
        max_length=100,
        db_index=True
    )

    terminal_id = models.CharField(
        max_length=100,
        db_index=True
    )

    class Meta:
        ordering = ["serial_number"]

    def __str__(self):
        return f"{self.serial_number} | {self.branch.name}"



class ATMStatistic(BaseModel):

    atm = models.ForeignKey(
        ATM,
        on_delete=models.CASCADE,
        related_name="statistics"
    )

    period = models.DateField()

    expense = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0
    )

    income = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0
    )

    class Meta:
        unique_together = ("atm", "period")
        ordering = ["-period"]

    def __str__(self):
        return f"{self.atm} {self.period}"