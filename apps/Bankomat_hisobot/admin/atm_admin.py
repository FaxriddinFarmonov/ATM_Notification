from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html
from django.utils.formats import number_format
from django.http import HttpResponse
from django.urls import path
from ..services.excel_exporter import ATMExcelExporter
from django.urls import reverse
from django.utils.html import format_html
from ..services.full_excel_exporter import FullATMExcelExporter

from ..models import (
    ATMTURON, ATMYearStatistic,
)

from .inlines import (
    ATMMonthlyStatisticInline,
    ATMYearStatisticInline,
)
def make_income(year):

    @admin.display(description=f"{year} Income")
    def income(admin_self, obj):

        stat = next(
            (
                s
                for s in obj.year_statistics.all()
                if s.year == year
                and s.card_type == obj.card_type
            ),
            None,
        )

        if stat and stat.income:
            return f"{stat.income:,.3f}"

        total = (
            obj.monthly_statistics.filter(
                year=year,
            ).aggregate(
                total=Sum("income"),
            )["total"]
            or 0
        )

        return f"{total:,.3f}"

    return income
def make_expense(year):

    @admin.display(description=f"{year} Cash Withdraw")
    def expense(admin_self, obj):

        stat = next(
            (
                s
                for s in obj.year_statistics.all()
                if s.year == year
                and s.card_type == obj.card_type
            ),
            None,
        )

        if stat and stat.expense:
            return f"{stat.expense:,.3f}"

        total = (
            obj.monthly_statistics.filter(
                year=year,
            ).aggregate(
                total=Sum("expense"),
            )["total"]
            or 0
        )

        return f"{total:,.3f}"

    return expense
@admin.register(ATMTURON)
class ATMTURONAdmin(admin.ModelAdmin):
    inlines = (
        ATMMonthlyStatisticInline,
        ATMYearStatisticInline,
    )

    search_fields = (
        "terminal_id",
        "address",
        "region",
        "name",
        "model",
    )
    list_filter = (
        "region",
        "card_type",
        "model",
        "is_active",
        "created_at",
    )
    ordering = (
        "region",
        "terminal_id",
    )
    list_per_page = 50
    date_hierarchy = "created_at"
    save_on_top = True

    save_as = True
    readonly_fields = (
        "download_excel_button",
        "created_at",
        "updated_at",
    )
    fieldsets = (

        ("Asosiy ma'lumotlar", {

            "fields": (

                "terminal_id",

                "card_type",

                "region",

                "name",

                "address",

                "model",

            )

        }),
        (
            "Export",
            {
                "fields": (
                    "download_excel_button",
                ),
            },
        ),

        ("Holati", {

            "fields": (

                "is_active",

                "note",

            )

        }),

        ("Tizim", {

            "classes": (

                "collapse",

            ),

            "fields": (

                "created_at",

                "updated_at",

            )

        }),

    )

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "<int:object_id>/download-excel/",
                self.admin_site.admin_view(self.download_excel),
                name="atm_download_excel",
            ),
            path(
                "download-full-excel/",
                self.admin_site.admin_view(
                    self.download_full_excel
                ),
                name="atm_download_full_excel",
            ),
        ]

        return custom_urls + urls

    def download_excel(self, request, object_id):

        atm = self.get_object(request, object_id)

        exporter = ATMExcelExporter(atm)

        return exporter.build_response()

    @admin.display(description="")

    def download_full_excel(self, request):

        exporter = FullATMExcelExporter()

        output = exporter.export()

        response = HttpResponse(
            output.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        response[
            "Content-Disposition"
        ] = 'attachment; filename="All_ATMs_Report.xlsx"'

        return response
    
    def download_excel_button(self, obj):

        if not obj.pk:
            return "-"

        url = reverse(
            "admin:atm_download_excel",
            args=[obj.pk],
        )

        return format_html(
            """
            <a class="button"
               href="{}"
               style="
                    background:#198754;
                    color:white;
                    padding:10px 18px;
                    text-decoration:none;
                    border-radius:6px;
                    font-weight:bold;">
                ⬇ Download Excel
            </a>
            """,
            url,
        )
    def get_list_display(self, request):

        columns = [

            "terminal_id",

            "region",

            "card_type",

            "model",

        ]

        years = (
            ATMYearStatistic.objects
            .order_by("year")
            .values_list("year", flat=True)
            .distinct()
        )

        for year in years:

            income_name = f"income_{year}"
            expense_name = f"expense_{year}"

            # income metodini dinamik yaratamiz
            if not hasattr(self.__class__, income_name):
                setattr(
                    self.__class__,
                    income_name,
                    make_income(year),
                )

            if not hasattr(self.__class__, expense_name):
                setattr(
                    self.__class__,
                    expense_name,
                    make_expense(year),
                )
            columns.append(income_name)
            columns.append(expense_name)

        columns.append("is_active")

        return columns

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        return qs.prefetch_related(
            "monthly_statistics",
            "year_statistics",
        )
    @admin.display(description="Card")
    def card_badge(self, obj):

        if obj.card_type == "HUMO":

            color = "#2E86DE"

        else:

            color = "#16A085"

        return format_html(

            '<b style="color:{};">{}</b>',

            color,

            obj.card_type,

        )





    def income_2026(self, obj):

        value = obj.monthly_statistics.filter(
            year=2026,
        ).aggregate(
            total=Sum("income")
        )["total"]

        return value or 0

    income_2026.short_description = "2026 Income"
    income_2026.admin_order_field = "monthly_statistics__income"

    def expense_2026(self, obj):

        value = obj.monthly_statistics.filter(
            year=2026,
        ).aggregate(
            total=Sum("expense")
        )["total"]

        return value or 0

    expense_2026.short_description = "2026 Expense"
    expense_2026.admin_order_field = "monthly_statistics__expense"

    def income_2025(self, obj):

        value = obj.monthly_statistics.filter(
            year=2025,
        ).aggregate(
            total=Sum("income")
        )["total"]

        return value or 0

    def expense_2025(self, obj):

        value = obj.monthly_statistics.filter(
            year=2025,
        ).aggregate(
            total=Sum("expense")
        )["total"]

        return value or 0

