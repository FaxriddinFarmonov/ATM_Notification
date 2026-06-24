from django.contrib import admin

from apps.notifications.models import Notification

from django.contrib import admin
from django.utils.html import format_html
from .models import Notification
from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    # Jadvalda ko‘rinadigan ustunlar
    list_display = (
        "id",
        "chat_id",
        "status",
        "created_at",
    )

    # Global search (hamma maydonlar bo‘yicha)
    search_fields = (
        "id",
        "event__id",
        "event__atm__serial",   # ATM ga bog‘liq bo‘lsa
        "event__atm__tid",
        "chat_id",
        "text",
        "status",
    )

    # Filter panel
    list_filter = (
        "status",
        "created_at",
        "sent_at",
        "event",
    )

    # Default ordering
    ordering = ("-created_at",)

    # List ichida tez edit qilish
    list_editable = ("status",)

    # Pagination
    list_per_page = 25

    # Readonly fields (production uchun xavfsiz)
    readonly_fields = ("created_at", "sent_at")

    # Detail view grouping
    fieldsets = (
        ("Main Info", {
            "fields": ("event", "chat_id", "text")
        }),
        ("Status Info", {
            "fields": ("status", "sent_at")
        }),
        ("System Info", {
            "fields": ("created_at",),
        }),
    )

    # Textni qisqartirib ko‘rsatish
    def short_text(self, obj):
        return obj.text[:80] + "..." if obj.text and len(obj.text) > 80 else obj.text
    short_text.short_description = "Text"


    # Save vaqtida logika qo‘shish mumkin (kelajak uchun hook)
    def save_model(self, request, obj, form, change):
        # Masalan: audit log yoki validation
        super().save_model(request, obj, form, change)