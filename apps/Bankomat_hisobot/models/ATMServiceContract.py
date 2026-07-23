from django.db import models

from apps.Bankomat_hisobot.models.full_models import (
    ATMTURON,
)


class ATMServiceContract(models.Model):

    atm = models.OneToOneField(
        ATMTURON,
        on_delete=models.CASCADE,
        related_name="service_contract",
    )




    btech_monthly_fee = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0,
    )

    glob_monthly_fee = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = (
            "atm__terminal_id",
        )





    def __str__(self):

        return self.atm.terminal_id




class ATMServicePayment(models.Model):

    class PaymentType(models.TextChoices):

        INCASSATION = (
            "INCASSATION",
            "Incassation",
        )

        RENT = (
            "RENT",
            "Rent",
        )

        ELECTRICITY = (
            "ELECTRICITY",
            "Electricity",
        )

    contract = models.ForeignKey(
        ATMServiceContract,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    year = models.PositiveSmallIntegerField(
        db_index=True,
    )

    month = models.PositiveSmallIntegerField(
        db_index=True,
    )

    payment_type = models.CharField(
        max_length=30,
        choices=PaymentType.choices,
        db_index=True,
    )

    amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0,
    )

    class Meta:

        unique_together = (

            "contract",

            "year",

            "month",

            "payment_type",

        )

        ordering = (

            "-year",

            "-month",

        )

        indexes = [

            models.Index(
                fields=[
                    "year",
                    "month",
                ]
            ),

            models.Index(
                fields=[
                    "payment_type",
                ]
            ),

        ]

    def __str__(self):

        return (

            f"{self.contract.atm.terminal_id} "

            f"{self.year}-{self.month}"

        )
