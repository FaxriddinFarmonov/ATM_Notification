from rest_framework import serializers

from apps.maintenance.models import MaintenanceItem


class MaintenanceDetailSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = MaintenanceItem

        fields = "__all__"