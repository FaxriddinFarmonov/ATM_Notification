from django.contrib import admin

# Register your models here.

from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):

    save_on_top = True

    list_per_page = 50

    date_hierarchy = "created_at"

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )
