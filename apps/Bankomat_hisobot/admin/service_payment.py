from django.contrib import admin
from apps.Bankomat_hisobot.models import ATMServicePayment
from .payment_filters import (
    MonthFilter,
    BTechFilter,
    GlobFilter,
    ElectricityFilter,
    RentFilter,
    IncassationFilter,
)

MONTHS = {
    1: "Yanvar",
    2: "Fevral",
    3: "Mart",
    4: "Aprel",
    5: "May",
    6: "Iyun",
    7: "Iyul",
    8: "Avgust",
    9: "Sentabr",
    10: "Oktabr",
    11: "Noyabr",
    12: "Dekabr",
}


@admin.register(ATMServicePayment)
class ATMServicePaymentAdmin(admin.ModelAdmin):
    fields = (
        "contract",
        "payment_type",
        "year",
        "month",
        "amount",
    )
    list_display = (
        "terminal_id",
        "payment_name",
        "year",
        "month_name",
        "amount",
    )

    list_select_related = (
        "contract",
        "contract__atm",
    )

    ordering = (
        "-year",
        "-month",
    )

    list_per_page = 100

    search_fields = (
        "contract__atm__terminal_id",

    )
    list_filter = (
        "payment_type",
        "year",

        MonthFilter,


        BTechFilter,

        GlobFilter,

        ElectricityFilter,

        RentFilter,

        IncassationFilter,
    )

    autocomplete_fields = (
        "contract",
    )


    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
    @admin.display(
        description="Terminal ID",
        ordering="contract__atm__terminal_id",
    )
    def terminal_id(self, obj):
        return obj.contract.atm.terminal_id

    @admin.display(
        description="To'lov turi",
        ordering="payment_type",
    )
    def payment_name(self, obj):
        return obj.get_payment_type_display()

    @admin.display(
        description="Oy",
        ordering="month",
    )
    def month_name(self, obj):
        return MONTHS.get(obj.month, obj.month)


class ATMServicePaymentInline(admin.TabularInline):

    model = ATMServicePayment

    extra = 1

    fields = (
        "payment_type",
        "year",
        "month",
        "amount",
    )

    ordering = (
        "-year",
        "-month",
    )

    show_change_link = True