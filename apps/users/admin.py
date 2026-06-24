from django.contrib import admin

from apps.users.models import Engineer
from django.contrib import admin
from .models import Engineer


@admin.register(Engineer)
class EngineerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "phone",
        "telegram_chat_id",
        "telegram_username"
    )

    search_fields = (
        "id",
        "full_name",
        "phone",
        "telegram_chat_id",
        "telegram_username"
    )

    list_filter = (
        "full_name",
        "telegram_username"
    )

    ordering = ("full_name", "telegram_username")

    fieldsets = (
        ("👤 Engineer Info", {
            "fields": ("full_name", "phone", "telegram_chat_id", "telegram_username")
        }),
    )