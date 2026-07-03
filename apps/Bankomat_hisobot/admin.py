from django.contrib import admin

from .models import (
    Region,
    Branch,
    ATMType,
    ATMModel,
    ATM,
    ATMStatistic,
)


# ==========================================================
# BASE ADMIN
# ==========================================================

class BaseAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    list_per_page = 100

    save_on_top = True

    show_full_result_count = True

    date_hierarchy = "created_at"


# ==========================================================
# REGION
# ==========================================================

@admin.register(Region)
class RegionAdmin(BaseAdmin):

    list_display = (
        "name",
        "created_at",
    )

    search_fields = (
        "name",
    )


# ==========================================================
# BRANCH
# ==========================================================

@admin.register(Branch)
class BranchAdmin(BaseAdmin):

    list_display = (
        "region",
        "name",
        "legal_address",
    )

    search_fields = (
        "name",
        "legal_address",
        "region__name",
    )

    list_filter = (
        "region",
    )

    autocomplete_fields = (
        "region",
    )


# ==========================================================
# ATM TYPE
# ==========================================================

@admin.register(ATMType)
class ATMTypeAdmin(BaseAdmin):

    search_fields = ("name",)

    list_display = (
        "name",
    )


# ==========================================================
# ATM MODEL
# ==========================================================

@admin.register(ATMModel)
class ATMModelAdmin(BaseAdmin):

    list_display = (
        "name",
        "manufacturer",
    )

    search_fields = (
        "name",
        "manufacturer",
    )


# ==========================================================
# ATM
# ==========================================================

@admin.register(ATM)
class ATMAdmin(BaseAdmin):

    list_display = (

        "region",

        "branch",

        "atm_type",

        "atm_model",

        "status_badge",

        "serial_number",

        "inventory_number",

        "merchant_id",

        "terminal_id",

        "legal_address",

    )

    search_fields = (

        "serial_number",

        "inventory_number",

        "merchant_id",

        "terminal_id",

        "branch__name",

        "branch__legal_address",

        "branch__region__name",

    )

    list_filter = (

        "status",

        "atm_type",

        "atm_model",

        "branch__region",

    )

    autocomplete_fields = (

        "branch",

        "atm_type",

        "atm_model",

    )

    list_select_related = (

        "branch",

        "branch__region",

        "atm_type",

        "atm_model",

    )

    ordering = (

        "branch__region__name",

        "branch__name",

        "serial_number",

    )

    list_per_page = 100

    list_max_show_all = 1000

    list_display_links = (

        "serial_number",

    )

    actions = None

    # --------------------------

    @admin.display(ordering="branch__region__name", description="BXM")
    def region(self, obj):
        return obj.branch.region.name

    # --------------------------

    @admin.display(ordering="branch__name", description="Joylashgan joyi")
    def branch(self, obj):
        return obj.branch.name

    # --------------------------

    @admin.display(description="Yuridik manzili")
    def legal_address(self, obj):
        return obj.branch.legal_address

    # --------------------------

    @admin.display(
        description="Holati",
        ordering="status"
    )
    def status_badge(self, obj):

        if obj.status == "active":

            return "✅ Soz"

        return "❌ Nosoz"


# ==========================================================
# ATM STATISTIC
# ==========================================================

@admin.register(ATMStatistic)
class ATMStatisticAdmin(BaseAdmin):

    list_display = (

        "atm",

        "period",

        "expense",

        "income",

    )

    autocomplete_fields = (

        "atm",

    )

    search_fields = (

        "atm__serial_number",

        "atm__merchant_id",

        "atm__terminal_id",

    )

    list_filter = (

        "period",

    )

    list_select_related = (

        "atm",

    )