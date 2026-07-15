from rest_framework import serializers

from apps.Bankomat_hisobot.models.ATMMonthlyStatistic import ATMTURON
class ATMListSerializer(serializers.ModelSerializer):

    terminal_id = serializers.CharField(
        source="technical.terminal_id",
        read_only=True,
    )

    merchant_id = serializers.CharField(
        source="technical.merchant_id",
        read_only=True,
    )

    serial_number = serializers.CharField(
        source="technical.serial_number",
        read_only=True,
    )

    status = serializers.CharField(
        source="technical.status",
        read_only=True,
    )

    card_type = serializers.CharField(
        source="technical.card_type",
        read_only=True,
    )

    model = serializers.CharField(
        source="technical.model_name",
        read_only=True,
    )

    address = serializers.CharField(
        source="technical.address",
        read_only=True,
    )

    class Meta:
        model = ATMTURON

        fields = (
            "id",
            "name",
            "region",
            "terminal_id",
            "merchant_id",
            "serial_number",
            "status",
            "card_type",
            "model",
            "address",
        )
