from django.db import models
from django.core.validators import FileExtensionValidator


import os
from django.db import models

from apps.Bankomat_hisobot.models.full_models import ATMTechnical

class DocumentUpload(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name="Hujjat nomi")
    file = models.FileField(upload_to="uploaded_protocols/%Y/%m/", verbose_name="PDF fayl")
    is_processed = models.BooleanField(default=False, verbose_name="Active")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuklangan vaqti")

    def save(self, *args, **kwargs):
        if not self.title and self.file:
            filename = os.path.basename(self.file.name)
            self.title = os.path.splitext(filename)[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class MaintenanceProtocol(models.Model):
    document_source = models.OneToOneField(DocumentUpload, on_delete=models.CASCADE, related_name="protocol_data", verbose_name="Manba hujjat")
    protocol_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Protokol raqami", db_index=True)
    protocol_date = models.DateField(verbose_name="Protokol sanasi", db_index=True)
    performer_company = models.CharField(max_length=255, default="VTECH MCHJ", verbose_name="Ijrochi tashkilot")
    customer_bank = models.CharField(max_length=255, default="TURON BANK ATB", verbose_name="Buyurtmachi bank")

    class Meta:
        verbose_name = "Jadval"
        verbose_name_plural = "Jadvallar"

    def __str__(self):
        return f"Protokol {self.protocol_number} - {self.protocol_date}"

class MaintenanceItem(models.Model):
    document = models.ForeignKey(DocumentUpload, on_delete=models.CASCADE, related_name="items", verbose_name="Hujjat", null=True, blank=True)
    protocol = models.ForeignKey(MaintenanceProtocol, on_delete=models.CASCADE, related_name="items", verbose_name="Protokol", null=True, blank=True)
    row_number = models.IntegerField(verbose_name="№")
    protocol_date = models.DateField(null=True, blank=True, verbose_name="Hujjat sanasi")
    equipment_module = models.CharField(max_length=100, blank=True, default="", verbose_name="Модуль оборудования")
    serial_number = models.CharField(max_length=100, blank=True, default="", db_index=True, verbose_name="Серийный номер")
    technical = models.ForeignKey(
        ATMTechnical,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenance_items",
    )
    filial_name = models.CharField(max_length=255, blank=True, default="", verbose_name="Наименование филиала")
    mfo_bank = models.CharField(max_length=20, blank=True, default="", verbose_name="МФО банка")

    part_name = models.TextField(verbose_name="Наименование запчастей", db_index=True)
    measurement_unit = models.CharField(max_length=50, verbose_name="O'lchov birligi", default="услуга (сум)")
    quantity = models.DecimalField(max_digits=12, decimal_places=4, verbose_name="Кол-во")
    price_per_unit = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Цена (СУМ)")
    total_amount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Сумма (СУМ)")
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="QQS (%)", default=12.00)
    vat_amount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Сумма НДС")
    total_with_vat = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Стоимость с учетом НДС")

    class Meta:
        verbose_name = "Umumiy ma'lumot"
        verbose_name_plural = "Umumiy ma'lumotlar"
        ordering = ['row_number']

    def __str__(self):
        return " "