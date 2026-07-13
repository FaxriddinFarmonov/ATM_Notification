from django.contrib import admin
from django.db.models import Sum
from ..models import (
    ATMMonthlyStatistic,
    ATMYearStatistic,
)

class ATMMonthlyStatisticInline(admin.TabularInline):
    """
    ATM ichida barcha oylik statistikalarni ko'rsatadi.
    """

    model = ATMMonthlyStatistic

    extra = 0

    can_delete = False

    show_change_link = True
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

    @admin.display(description="Oy")
    def month_name(self, obj):
        return self.MONTH_NAMES.get(obj.month, str(obj.month))

    ordering = (
        "year",
        "month",
    )

    fields = (
        "year",
        "month_name",
        "income_display",
        "expense_display",
    )

    readonly_fields = (
        "year",
        "month_name",
        "income_display",
        "expense_display",
    )

    @admin.display(description="Income")
    def income_display(self, obj):
        return f"{obj.income:,.3f}"

    @admin.display(description="Cash Withdraw")
    def expense_display(self, obj):
        return f"{obj.expense:,.3f}"

class ATMYearStatisticInline(admin.TabularInline):
    """
    ATM ichida barcha yillik statistikalarni ko'rsatadi.
    """

    model = ATMYearStatistic

    extra = 0

    can_delete = False

    show_change_link = True

    ordering = (
        "year",
        "card_type",
    )

    fields = (
        "year",
        "card_type",
        "income_display",
        "expense_display",
    )
    readonly_fields = (
        "year",
        "card_type",
        "income_display",
        "expense_display",
    )

    @admin.display(description="Income")
    def income_display(self, obj):
        return f"{obj.income:,.3f}"

    @admin.display(description="Cash Withdraw")
    def expense_display(self, obj):
        return f"{obj.expense:,.3f}"




    # total_expense.short_description = "Expense"

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

    @admin.display(description="Oy")
    def month_name(self, obj):
        return self.MONTHS.get(obj.month, obj.month)



class MonthlyStatisticInline(admin.TabularInline):
    model = ATMMonthlyStatistic

    extra = 0

    can_delete = False

    ordering = (
        "year",
        "month",
    )

    fields = (
        "year",
        "month_name",
        "income_display",
        "expense_display",
        "difference",
    )

    readonly_fields = fields

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

    def month_name(self, obj):
        return self.MONTH_NAMES.get(obj.month)

    month_name.short_description = "Oy"

    def income_display(self, obj):
        return f"{obj.income:,.3f}"

    income_display.short_description = "Daromad"

    def expense_display(self, obj):
        return f"{obj.expense:,.3f}"

    expense_display.short_description = "Chiqim"

    def difference(self, obj):
        return f"{obj.income - obj.expense:,.3f}"

    difference.short_description = "Farq"