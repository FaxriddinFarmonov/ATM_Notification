from rest_framework import serializers

from apps.maintenance.models import MaintenanceItem


class MaintenanceListSerializer(
    serializers.ModelSerializer
):

    atm_id = serializers.IntegerField(
        source="technical.atm.id",
        read_only=True,
        allow_null=True,
    )

    terminal_id = serializers.CharField(
        source="technical.terminal_id",
        read_only=True,
        allow_null=True,
    )

    atm_name = serializers.CharField(
        source="technical.atm.name",
        read_only=True,
        allow_null=True,
    )

    region = serializers.CharField(
        source="technical.atm.region",
        read_only=True,
        allow_null=True,
    )

    model = serializers.CharField(
        source="technical.model_name",
        read_only=True,
        allow_null=True,
    )

    card_type = serializers.CharField(
        source="technical.card_type",
        read_only=True,
        allow_null=True,
    )

    status = serializers.CharField(
        source="technical.status",
        read_only=True,
        allow_null=True,
    )

    protocol_number = serializers.CharField(
        source="protocol.protocol_number",
        read_only=True,
        allow_null=True,
    )

    class Meta:

        model = MaintenanceItem

        fields = (
            "id",

            "row_number",

            "protocol_number",
            "protocol_date",

            "atm_id",
            "terminal_id",
            "atm_name",
            "region",

            "model",
            "card_type",
            "status",

            "equipment_module",
            "serial_number",

            "filial_name",
            "mfo_bank",

            "part_name",
            "measurement_unit",

            "quantity",
            "price_per_unit",
            "total_amount",

            "vat_rate",
            "vat_amount",
            "total_with_vat",
        )