from django.db import models

class Engineer(models.Model):

    full_name = models.CharField(max_length=255)

    telegram_chat_id = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    telegram_username = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    phone = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.full_name