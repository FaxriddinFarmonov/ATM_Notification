from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html
from ..models import ATMTechnical, ATMImportFile
from ..importers.atm_importer import ATMExcelImporter
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages

from pathlib import Path

@admin.register(ATMTechnical)
class ATMAdmin(admin.ModelAdmin):
    change_list_template = "admin/Bankomat_hisobot/atmturon/change_texnik.html"

    list_display = (
        "terminal_id",
        "merchant_id",
        "colored_card_type",
        "model_name",
        "colored_status",
        "serial_number",
        "inventory_number",
        "short_address",
        "updated_at",
    )

    list_display_links = (
        "terminal_id",
    )

    ordering = (
        "terminal_id",
    )

    list_per_page = 50

    search_fields = (
        "terminal_id",
        "merchant_id",
        "serial_number",
        "inventory_number",
        "address",
        "model_name",
    )

    list_filter = (
        "card_type",
        "status",
        "model_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    save_on_top = True

    list_select_related = ()

    fieldsets = (
        (
            "ATM",
            {
                "fields": (
                    (
                        "card_type",
                        "status",
                    ),
                    (
                        "model_name",
                        "terminal_id",
                    ),
                    (
                        "merchant_id",
                        "serial_number",
                    ),
                    (
                        "inventory_number",
                    ),
                    "address",
                )
            },
        ),
        (
            "Hisoblar",
            {
                "fields": (
                    (
                        "account_23510",
                        "account_45265",
                    ),
                )
            },
        ),
        (
            "Tizim",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    @admin.display(description="Status", ordering="status")
    def colored_status(self, obj):

        if obj.status == "SOZ":
            color = "#198754"
        else:
            color = "#dc3545"

        return format_html(
            '<strong style="color:{};">{}</strong>',
            color,
            obj.get_status_display(),
        )

    @admin.display(description="Card", ordering="card_type")
    def colored_card_type(self, obj):

        colors = {
            "UZCARD": "#0d6efd",
            "HUMO": "#6f42c1",
            "VASH": "#fd7e14",
        }

        return format_html(
            '<strong style="color:{};">{}</strong>',
            colors.get(obj.card_type, "#000"),
            obj.card_type,
        )

    @admin.display(description="Address")
    def short_address(self, obj):

        if len(obj.address) <= 40:
            return obj.address

        return obj.address[:40] + "..."

    def changelist_view(self, request, extra_context=None):

        extra_context = extra_context or {}

        qs = ATMTechnical.objects.all()

        extra_context["summary"] = {
            "total": qs.count(),
            "soz": qs.filter(status="SOZ").count(),
            "nosoz": qs.filter(status="NOSOZ").count(),
            "uzcard": qs.filter(card_type="UZCARD").count(),
            "humo": qs.filter(card_type="HUMO").count(),
            "vash": qs.filter(card_type="VASH").count(),
        }

        return super().changelist_view(
            request,
            extra_context=extra_context
        )

    def get_urls(self):

        urls = super().get_urls()

        custom_urls = [
            path(
                "update-excel/",
                self.admin_site.admin_view(
                    self.update_excel
                ),
                name="update-excel",
            ),
        ]

        return custom_urls + urls

    def update_excel(self, request):

        import_dir = Path(settings.MEDIA_ROOT) / "atm" / "imports"

        excel_files = list(import_dir.glob("*.xlsx"))

        if not excel_files:
            self.message_user(
                request,
                "Import papkasida Excel fayl topilmadi!",
                level=messages.ERROR,
            )
            return redirect(
                "admin:Bankomat_hisobot_atmtechnical_changelist"
            )

        # Eng oxirgi yuklangan fayl
        excel_path = max(excel_files, key=lambda f: f.stat().st_mtime)

        result = ATMExcelImporter(str(excel_path)).run()

        self.message_user(
            request,
            f"{excel_path.name} import qilindi. "
            f"Yangi: {result['created']} | "
            f"Yangilandi: {result['updated']}",
            level=messages.SUCCESS,
        )

        return redirect(
            "admin:Bankomat_hisobot_atmtechnical_changelist"
        )
@admin.register(ATMImportFile)
class ATMImportFileAdmin(admin.ModelAdmin):

    list_display = (
        "file",
        "created_at",
        "is_processed",
        "result",
    )


    def save_model(self, request, obj, form, change):

        super().save_model(
            request,
            obj,
            form,
            change
        )


        result = ATMExcelImporter(
            obj.file.path
        ).run()


        obj.is_processed = True

        obj.result = (
            f"Created: {result['created']} | "
            f"Updated: {result['updated']}"
        )


        obj.save()