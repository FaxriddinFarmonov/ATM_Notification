from .models import ATMEvent
from django.contrib import admin


from .models import (
    ATM,
    ATMCurrentState,
    # MonitoringSnapshot,
    ATMEvent,


)

# =========================
# 🔥 BASE ADMIN (ARCHITECTURE)
# =========================
class BaseAdmin(admin.ModelAdmin):
    """
    Senior-level reusable admin base.
    """
    list_per_page = 25
    save_on_top = True
    empty_value_display = "—"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(self, "select_related_fields"):
            qs = qs.select_related(*self.select_related_fields)
        if hasattr(self, "prefetch_related_fields"):
            qs = qs.prefetch_related(*self.prefetch_related_fields)
        return qs


# =========================
# 🔥 INLINE ADMINS
# =========================
class ATMCurrentStateInline(admin.StackedInline):
    model = ATMCurrentState
    extra = 0
    can_delete = False



class ATMEventInline(admin.TabularInline):
    model = ATMEvent
    extra = 0
    readonly_fields = ("event_type", "message", "created_at")
    can_delete = False




# =========================
# 🔥 ATM ADMIN (CORE)
# =========================
@admin.register(ATM)
class ATMAdmin(BaseAdmin):

    list_display = (
        "serial",
        "mfo",
        "merchant_id",
        "terminal_id",
        "host_provider",
        "branch_number",
        "model_name",
        "engineer",
    )
    search_fields = (
        "serial",
        "tid",
        "terminal_id",
        "branch_number",
        "address",
        "model_name",
        "responsible_engineer__full_name",
        "responsible_engineer__username",
    )

    list_filter = (
        "model_name",
        "branch_number",
        "responsible_engineer",
    )

    autocomplete_fields = ("responsible_engineer",)

    select_related_fields = ("responsible_engineer",)

    inlines = (
        ATMCurrentStateInline,

        ATMEventInline,
    )

    fieldsets = (
        ("🔑 Identifiers", {
            "fields": ("external_id", "atm_uid", "serial", "tid")
        }),
        ("📍 Location", {
            "fields": ("branch_number", "address")
        }),
        ("⚙️ Info", {
            "fields": ("model_name", "responsible_engineer", "extra_attrs")
        }),
    )
    @admin.display(description="MFO", ordering="extra_attrs")
    def mfo(self, obj):
        return (obj.extra_attrs or {}).get("mfo", "—")

    @admin.display(description="Merchant ID", ordering="extra_attrs")
    def merchant_id(self, obj):
        return (obj.extra_attrs or {}).get("merchantId", "—")

    @admin.display(description="Terminal ID", ordering="extra_attrs")
    def terminal_id(self, obj):
        return (obj.extra_attrs or {}).get("terminalId", "—")

    @admin.display(description="Host Provider", ordering="extra_attrs")
    def host_provider(self, obj):
        return (obj.extra_attrs or {}).get("hostProvider", "—")
    def engineer(self, obj):
        if obj.responsible_engineer:
            return obj.responsible_engineer
        return "—"




# =========================
# 🔥 ATM CURRENT STATE
# =========================
@admin.register(ATMCurrentState)
class ATMCurrentStateAdmin(BaseAdmin):
    list_display = (
        "atm",
        "agent_status",
        "service_status",
        "app_status",
        "cash_amount",
        "last_online",
        "updated_at",
    )

    search_fields = (
        "atm__serial",
        "atm__tid",
    )

    list_filter = (
        "agent_status",
        "service_status",
        "app_status",
    )

    select_related_fields = ("atm",)


# =========================
# 🔥 ATM EVENT (TO‘G‘RI)
# =========================
@admin.register(ATMEvent)
class ATMEventAdmin(admin.ModelAdmin):

    list_display = (
        "atm",
        "event_type",
        "is_sent",
        "created_at",
    )

    list_filter = ("event_type", "is_sent")

    search_fields = (
        "atm__serial",
        "atm__tid",
        "message",
    )
# =========================
# 🔥 CARD CASSETTE
