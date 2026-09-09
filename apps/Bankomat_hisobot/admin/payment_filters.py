from django.contrib.admin import SimpleListFilter


class MonthFilter(SimpleListFilter):
    title = "Oy"
    parameter_name = "month"

    MONTHS = (
        (1, "Yanvar"),
        (2, "Fevral"),
        (3, "Mart"),
        (4, "Aprel"),
        (5, "May"),
        (6, "Iyun"),
        (7, "Iyul"),
        (8, "Avgust"),
        (9, "Sentabr"),
        (10, "Oktabr"),
        (11, "Noyabr"),
        (12, "Dekabr"),
    )

    def lookups(self, request, model_admin):
        return self.MONTHS

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(month=self.value())
        return queryset


class BTechFilter(SimpleListFilter):
    title = "BTECH"

    parameter_name = "btech"

    def lookups(self, request, model_admin):
        return (
            ("yes", "BTECH mavjud"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(
                contract__btech_monthly_fee__gt=0
            )
        return queryset


class GlobFilter(SimpleListFilter):
    title = "GLOB"

    parameter_name = "glob"

    def lookups(self, request, model_admin):
        return (
            ("yes", "GLOB mavjud"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(
                contract__glob_monthly_fee__gt=0
            )
        return queryset


class ElectricityFilter(SimpleListFilter):
    title = "Elektr"

    parameter_name = "electricity"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Elektr mavjud"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(
                payment_type="ELECTRICITY",
                amount__gt=0,
            )
        return queryset


class RentFilter(SimpleListFilter):
    title = "Ijara"

    parameter_name = "rent"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Ijara mavjud"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(
                payment_type="RENT",
                amount__gt=0,
            )
        return queryset


class IncassationFilter(SimpleListFilter):
    title = "Inkasatsiya"
    parameter_name = "incassation"

 
    def lookups(self, request, model_admin):
        return (
            ("yes", "Inkasatsiya mavjud"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(
                payment_type="INCASSATION",
                amount__gt=0,
            )
        return queryset