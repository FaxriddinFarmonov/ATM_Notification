from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from ..models import ExcelImport
from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import get_object_or_404, redirect
from django.utils.html import format_html
from ..services.excel_importer import ATMExcelImporter
from ..models import ExcelImport

@admin.register(ExcelImport)
class ExcelImportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "file_name",
        "created_at",
        "success_badge",
        "run_import_button",
    )

    readonly_fields = (
        "created_at",
        "imported_rows",
        "success",
        "error",
    )

    search_fields = (
        "file",
    )

    ordering = (
        "-created_at",
    )

    list_filter = (
        "success",
        "created_at",
    )

    fieldsets = (
        (
            "Excel fayl",
            {
                "fields": (
                    "file",
                )
            },
        ),
        (
            "Natija",
            {
                "fields": (
                    "imported_rows",
                    "success",
                    "error",
                    "created_at",
                )
            },
        ),
    )

    def file_name(self, obj):
        return obj.file.name.split("/")[-1]

    file_name.short_description = "Excel File"

    def run_import_button(self, obj):
        return format_html(
            '<a class="button" '
            'style="background:#198754;color:white;'
            'padding:6px 12px;border-radius:5px;'
            'text-decoration:none;font-weight:bold;" '
            'href="run-import/{}/">'
            '▶ RUN IMPORT'
            '</a>',
            obj.id,
        )

    run_import_button.short_description = "Run"

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [

            path(

                "run-import/<int:pk>/",

                self.admin_site.admin_view(self.run_import),

                name="excel-run-import",

            ),

        ]

        return custom_urls + urls

    def run_import(self, request, pk):

        obj = get_object_or_404(
            ExcelImport,
            pk=pk,
        )

        try:

            ATMExcelImporter(obj).run()

            obj.success = True
            obj.error = ""
            obj.save(update_fields=[
                "success",
                "error",
            ])

            self.message_user(

                request,

                "✅ Excel muvaffaqiyatli import qilindi.",

                level=messages.SUCCESS,

            )

        except Exception as e:

            obj.success = False
            obj.error = str(e)

            obj.save(update_fields=[
                "success",
                "error",
            ])

            self.message_user(

                request,

                f"❌ {e}",

                level=messages.ERROR,

            )

        return redirect(
            "admin:Bankomat_hisobot_excelimport_changelist"
        )


    def success_badge(self, obj):
        if obj.success:
            return mark_safe(
                '<span style="color:white;background:#28a745;'
                'padding:4px 8px;border-radius:5px;">SUCCESS</span>'
            )

        return mark_safe(
            '<span style="color:white;background:#dc3545;'
            'padding:4px 8px;border-radius:5px;">FAILED</span>'
        )

    success_badge.short_description = "Status"