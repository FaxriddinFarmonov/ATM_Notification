from rest_framework import serializers


class DashboardSummarySerializer(serializers.Serializer):
    total_atms = serializers.IntegerField(help_text="Jami bankomatlar soni")
    active = serializers.IntegerField(help_text="Faol bankomatlar soni")
    inactive = serializers.IntegerField(help_text="Nofaol bankomatlar soni")
    soz = serializers.IntegerField(help_text="Soz bankomatlar soni")
    nosoz = serializers.IntegerField(help_text="Nosoz bankomatlar soni")
    uzcard = serializers.IntegerField(help_text="UZCARD bankomatlar soni")
    humo = serializers.IntegerField(help_text="HUMO bankomatlar soni")


class DashboardFinanceSerializer(serializers.Serializer):
    income = serializers.FloatField(help_text="Jami daromad (so'mda)")
    expense = serializers.FloatField(help_text="Jami xarajat (so'mda)")
    profit = serializers.FloatField(help_text="Sof foyda (so'mda)")


class DashboardMaintenanceSerializer(serializers.Serializer):
    repair_count = serializers.IntegerField(help_text="Ta'mirlashlar soni")
    repair_cost = serializers.FloatField(help_text="Ta'mirlash xarajatlari (so'mda)")


class DashboardTopRegionItemSerializer(serializers.Serializer):
    region = serializers.CharField(help_text="Viloyat nomi")
    total = serializers.IntegerField(help_text="Jami bankomatlar")
    active = serializers.IntegerField(help_text="Faol bankomatlar")
    inactive = serializers.IntegerField(help_text="Nofaol bankomatlar")
    soz = serializers.IntegerField(help_text="Soz bankomatlar")
    nosoz = serializers.IntegerField(help_text="Nosoz bankomatlar")
    uzcard = serializers.IntegerField(help_text="UZCARD soni")
    humo = serializers.IntegerField(help_text="HUMO soni")


class ChartNameValueSerializer(serializers.Serializer):
    name = serializers.CharField(help_text="Nomi / kategoriyasi")
    value = serializers.IntegerField(help_text="Miqdori")


class MonthlyChartItemSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    income = serializers.FloatField()
    expense = serializers.FloatField()
    profit = serializers.FloatField()


class RegionFinanceItemSerializer(serializers.Serializer):
    region = serializers.CharField()
    income = serializers.FloatField()
    profit = serializers.FloatField()


class TopModelItemSerializer(serializers.Serializer):
    model = serializers.CharField()
    total = serializers.IntegerField()
    soz = serializers.IntegerField()
    nosoz = serializers.IntegerField()


class RepairTrendItemSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    repair_count = serializers.IntegerField()
    repair_cost = serializers.FloatField()


class RecentMaintenanceATMSerializer(serializers.Serializer):
    terminal_id = serializers.CharField(allow_null=True)
    serial_number = serializers.CharField(allow_null=True)
    region = serializers.CharField(allow_null=True)


class RecentMaintenanceItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    protocol_number = serializers.CharField(allow_null=True)
    protocol_date = serializers.DateField(allow_null=True)
    part_name = serializers.CharField()
    quantity = serializers.FloatField()
    total_amount = serializers.FloatField()
    atm = RecentMaintenanceATMSerializer()


class DashboardSerializer(serializers.Serializer):
    summary = DashboardSummarySerializer()
    finance = DashboardFinanceSerializer()
    maintenance = DashboardMaintenanceSerializer()
    top_regions = DashboardTopRegionItemSerializer(many=True)
    status_chart = ChartNameValueSerializer(many=True)
    card_chart = ChartNameValueSerializer(many=True)
    monthly_chart = MonthlyChartItemSerializer(many=True)
    region_finance = RegionFinanceItemSerializer(many=True)
    top_models = TopModelItemSerializer(many=True)
    repair_trend = RepairTrendItemSerializer(many=True)
    recent_maintenance = RecentMaintenanceItemSerializer(many=True)