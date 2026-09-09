from django.contrib import admin
from apps.users.models import Engineer
from apps.atms.models import ATM


class AssignedATMInline(admin.TabularInline):
    model = ATM
    fk_name = "responsible_engineer"
    fields = ("serial", "tid", "model_name", "branch_number", "address")
    readonly_fields = ("serial", "tid", "model_name", "branch_number", "address")
    extra = 0
    show_change_link = True
    can_delete = True


@admin.register(Engineer)
class EngineerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "region",
        "specialization",
        "phone",
        "telegram_username",
        "is_active",
    )

    search_fields = (
        "id",
        "full_name",
        "first_name",
        "last_name",
        "phone",
        "telegram_username",
        "region",
        "specialization",
    )

    list_filter = (
        "region",
        "specialization",
        "is_active",
    )

    ordering = ("full_name",)
    inlines = [AssignedATMInline]

    fieldsets = (
        ("👤 Engineer Info", {
            "fields": (
                ("first_name", "last_name", "patronymic"),
                "full_name",
                "region",
                "specialization",
                "avatar_url",
                "is_active",
            )
        }),
        ("📞 Contact Info", {
            "fields": ("phone", "telegram_chat_id", "telegram_username")
        }),
    )