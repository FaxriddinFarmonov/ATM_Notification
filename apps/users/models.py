from django.db import models

class Engineer(models.Model):
    first_name = models.CharField(max_length=100, blank=True, default="")
    last_name = models.CharField(max_length=100, blank=True, default="")
    patronymic = models.CharField(max_length=100, blank=True, default="")
    full_name = models.CharField(max_length=255, db_index=True)

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

    region = models.CharField(
        max_length=150,
        blank=True,
        default="",
        db_index=True,
        verbose_name="Hudud / Viloyat"
    )

    specialization = models.CharField(
        max_length=150,
        blank=True,
        default="ATM Servis Muhandisi",
        verbose_name="Mutaxassislik"
    )

    avatar_url = models.URLField(
        max_length=500,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Faol"
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if not self.full_name:
            names = [self.first_name, self.last_name, self.patronymic]
            computed = " ".join(filter(None, names)).strip()
            self.full_name = computed or "Texnik Muhandis"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.region or 'Hudud biriktirilmagan'})"