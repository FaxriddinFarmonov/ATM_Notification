from django.db import models

# Create your models here.
class ATM(models.Model):
    external_id = models.BigIntegerField(unique=True)

    atm_uid = models.CharField(max_length=255, null=True)

    serial = models.CharField(max_length=100, db_index=True)
    tid = models.CharField(max_length=100, db_index=True)

    extra_attrs = models.JSONField(null=True, blank=True)

    responsible_engineer = models.ForeignKey(
        "users.Engineer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    branch_number = models.CharField(max_length=50, null=True)
    address = models.TextField(null=True)



    model_name = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return f"{self.serial} - {self.address} - {self.model_name}"



class ATMCurrentState(models.Model):
    atm = models.OneToOneField(
        ATM,
        on_delete=models.CASCADE
    )

    agent_status = models.CharField(
        max_length=50
    )

    service_status = models.CharField(
        max_length=50
    )

    app_status = models.CharField(
        max_length=50
    )

    app_conn_status = models.CharField(
        max_length=50
    )

    cash_amount = models.BigIntegerField(
        default=0
    )

    last_online = models.DateTimeField(
        null=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"TID - {self.atm.tid} - Serial nomer  {self.atm.serial}"

class ATMEvent(models.Model):

    class EventType(models.TextChoices):
        CASH_LOW = "BANKOMATDA_PUL_KAM", "Cash low"
        NO_TRANSACTION = "TRANZAKSIYA_YO'Q", "No transaction"
        OFFLINE = "BANKOMAT_OFFLINE", "Offline"
        ONLINE = "BANKOMAT_ONLINE", "Online"

    atm = models.ForeignKey("ATM", on_delete=models.CASCADE, related_name="events")

    event_type = models.CharField(max_length=50, choices=EventType.choices)

    message = models.TextField()

    meta = models.JSONField(null=True, blank=True)

    is_sent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    # NEW
    status = models.CharField(
        max_length=20,
        default="PENDING"
    )

