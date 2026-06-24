from django.db import models


class Notification(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "PENDING"),
        ("SENT", "SENT"),
        ("FAILED", "FAILED"),
    )

    event = models.ForeignKey(
        "atms.ATMEvent",
        on_delete=models.CASCADE
    )

    chat_id = models.BigIntegerField()

    text = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("event", "chat_id")

    def __str__(self):
        return self.status