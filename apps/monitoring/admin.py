from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import MonitoringConfig


@admin.register(MonitoringConfig)
class MonitoringConfigAdmin(admin.ModelAdmin):
    list_display = (
        "updated_at",
    )