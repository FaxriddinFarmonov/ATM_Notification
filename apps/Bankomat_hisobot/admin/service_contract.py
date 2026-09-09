from django.contrib import admin
from django.db.models import Sum
from apps.Bankomat_hisobot.models import (
    ATMServiceContract,
)
from .service_payment import ATMServicePaymentInline

MONTH_NAMES = {
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
@admin.register(ATMServiceContract)
class ATMServiceContractAdmin(admin.ModelAdmin):
    list_display = (
        "terminal_id",

        "btech_monthly_fee",
        "glob_monthly_fee",

        "incassation_fee",
        "rent_fee",
        "electricity_fee",

        "last_payment",
        "payments_count",
    )
    inlines = (
        ATMServicePaymentInline,
    )
    list_select_related = (
        "atm",
    )

    ordering = (
        "atm__terminal_id",
    )

    list_per_page = 100

    search_fields = (
        "atm__terminal_id",

    )

    autocomplete_fields = (
        "atm",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
    from django.db.models import Count

    @admin.display(description="Incassation")
    def incassation_fee(self, obj):
        payment = (
            obj.payments
            .filter(payment_type="INCASSATION")
            .order_by("-year", "-month")
            .first()
        )
        return payment.amount if payment else 0

    @admin.display(description="Rent")
    def rent_fee(self, obj):
        payment = (
            obj.payments
            .filter(payment_type="RENT")
            .order_by("-year", "-month")
            .first()
        )
        return payment.amount if payment else 0

    @admin.display(description="Electricity")
    def electricity_fee(self, obj):
        payment = (
            obj.payments
            .filter(payment_type="ELECTRICITY")
            .order_by("-year", "-month")
            .first()
        )
        return payment.amount if payment else 0

    @admin.display(description="Last payment")
    def last_payment(self, obj):
        payment = (
            obj.payments
            .order_by("-year", "-month")
            .first()
        )

        if not payment:
            return "-"

        return f"{payment.year}-{payment.month:02d}"

    @admin.display(description="Payments")
    def payments_count(self, obj):
        return obj.payments.count()

    def month_name(self, obj):
        return MONTH_NAMES.get(obj.month, obj.month)

    month_name.short_description = "Oy"
    month_name.admin_order_field = "month"

    def terminal_id(self, obj):
        return obj.atm.terminal_id

    terminal_id.admin_order_field = "atm__terminal_id"

    def total_payment(self, obj):

        result = obj.payments.aggregate(
            total=Sum("amount")
        )

        return result["total"] or 0

