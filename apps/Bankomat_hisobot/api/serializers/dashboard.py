from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):
    total_atms = serializers.IntegerField()

    active = serializers.IntegerField()
    inactive = serializers.IntegerField()

    soz = serializers.IntegerField()
    nosoz = serializers.IntegerField()

    uzcard = serializers.IntegerField()
    humo = serializers.IntegerField()

    total_income = serializers.DecimalField(
        max_digits=20,
        decimal_places=3,
    )

    total_expense = serializers.DecimalField(
        max_digits=20,
        decimal_places=3,
    )

    repair_cost = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    repair_count = serializers.IntegerField()