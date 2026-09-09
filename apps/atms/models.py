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
        blank=True,
        related_name="assigned_atms"
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


class BTechConfig(models.Model):
    bearer_token = models.TextField(
        verbose_name="BTech Bearer Token",
        help_text="Har 3 kunda yangilanadigan BTech JWT Bearer Token (Bearer so'zi bilan yoki uningsiz kiriting)",
        default="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjM2NiwiaWF0IjoxNzg4ODM5NzA3LCJleHAiOjE3ODkwOTg5MDcsImp0aSI6IjNiY2JhMmNhLWFkMTktNDUyOC1iN2YxLTg1OTEwMTIwNmMwMCJ9.2YiXTsWyveVXdIhY2SrhcJrXvtq3UfmaAV8NfU2_qQg"
    )
    api_url = models.CharField(
        max_length=500,
        default="https://monitoring.btech.uz/api/base/atm/?clientId=&vendorId=&modelId=&functionId=&variantId=&atmGroupId=&countryId=&regionId=&cityId=&hashTags=&appConnectionStatus=all&agentConnectionStatus=online&hwFaults=&atmStatus=production&withUnitsTurnoverTotal=true&offset=0&limit=500&lang=en",
        verbose_name="BTech API URL"
    )
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    last_synced_at = models.DateTimeField(null=True, blank=True, verbose_name="Oxirgi sinxronizatsiya vaqti")
    last_sync_status = models.CharField(max_length=150, default="NOT_SYNCED", verbose_name="Oxirgi sinxronizatsiya holati")

    class Meta:
        verbose_name = "BTech Token Config"
        verbose_name_plural = "BTech Token Configs"

    def __str__(self):
        return f"BTech Config (Active: {self.is_active}, Last Sync: {self.last_synced_at})"


class BTechATMSnapshot(models.Model):
    btech_id = models.BigIntegerField(unique=True, db_index=True)
    serial = models.CharField(max_length=100, db_index=True)
    tid = models.CharField(max_length=100, db_index=True, blank=True, default="")
    status = models.CharField(max_length=50, default="production")
    service_status = models.CharField(max_length=50, default="InService")
    app_conn_status = models.CharField(max_length=50, default="Online")
    agent_status = models.CharField(max_length=50, default="online")
    last_online = models.DateTimeField(null=True, blank=True)

    total_cash_uzs = models.BigIntegerField(default=0)
    total_cash_usd = models.BigIntegerField(default=0)

    address = models.TextField(blank=True, default="")
    model_name = models.CharField(max_length=255, blank=True, default="")
    vendor_name = models.CharField(max_length=255, blank=True, default="")
    branch_number = models.CharField(max_length=50, blank=True, default="")

    raw_data = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        verbose_name = "BTech ATM Snapshot"
        verbose_name_plural = "BTech ATM Snapshots"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.tid or self.serial} - {self.service_status}"


