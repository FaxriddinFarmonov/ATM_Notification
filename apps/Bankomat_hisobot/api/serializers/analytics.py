from rest_framework import serializers

from ..swagger_constants import (
    AVAILABLE_REGIONS,
    AVAILABLE_YEARS,
    AVAILABLE_MONTHS,
    CARD_TYPE_CHOICES,
    SORT_BY_CHOICES,
    PERIOD_CHOICES,
    EXPENSE_TYPE_CHOICES,
)


class TopRegionsFilterSerializer(serializers.Serializer):
    year = serializers.ChoiceField(
        choices=AVAILABLE_YEARS,
        required=False,
        allow_null=True,
        help_text="Filtrlash uchun yilni tanlang (bo'sh qoldirilsa, oxirgi davr olinadi)"
    )
    month = serializers.ChoiceField(
        choices=AVAILABLE_MONTHS,
        required=False,
        allow_null=True,
        help_text="Filtrlash uchun oyni tanlang (1-12)"
    )
    sort_by = serializers.ChoiceField(
        choices=["income", "expense", "profit", "profit_margin", "atms_count", "cash_withdrawal"],
        default="income",
        required=False,
        help_text="Saralash ustuni: income, expense, profit, profit_margin, atms_count, cash_withdrawal"
    )
    limit = serializers.IntegerField(
        default=20,
        required=False,
        min_value=1,
        max_value=500,
        help_text="Natijalar soni chegarasi (default: 20)"
    )


class TopIncomeFilterSerializer(serializers.Serializer):
    period = serializers.ChoiceField(
        choices=PERIOD_CHOICES,
        default="all",
        required=False,
        help_text="Davr turi: all (umumiy), yearly (yillik), monthly (oylik)"
    )
    year = serializers.ChoiceField(
        choices=AVAILABLE_YEARS,
        required=False,
        allow_null=True,
        help_text="Yilni tanlang"
    )
    month = serializers.ChoiceField(
        choices=AVAILABLE_MONTHS,
        required=False,
        allow_null=True,
        help_text="Oyni tanlang (1-12)"
    )
    region = serializers.ChoiceField(
        choices=AVAILABLE_REGIONS,
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="Viloyatni tanlang"
    )
    card_type = serializers.ChoiceField(
        choices=CARD_TYPE_CHOICES,
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="Karta turini tanlang (UZCARD yoki HUMO)"
    )
    limit = serializers.IntegerField(
        default=10,
        required=False,
        min_value=1,
        max_value=500,
        help_text="Qaytariladigan bankomatlar soni (default: 10)"
    )


class TopExpenseFilterSerializer(serializers.Serializer):
    expense_type = serializers.ChoiceField(
        choices=["all", "maintenance", "rent", "electricity", "incassation"],
        default="all",
        required=False,
        help_text="Xarajat turi: all (jami), maintenance (ta'mirlash/zapchast), rent (ijara), electricity (elektr), incassation (inkassatsiya)"
    )
    year = serializers.ChoiceField(
        choices=AVAILABLE_YEARS,
        required=False,
        allow_null=True,
        help_text="Yilni tanlang"
    )
    month = serializers.ChoiceField(
        choices=AVAILABLE_MONTHS,
        required=False,
        allow_null=True,
        help_text="Oyni tanlang"
    )
    region = serializers.ChoiceField(
        choices=AVAILABLE_REGIONS,
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="Viloyatni tanlang"
    )
    limit = serializers.IntegerField(
        default=10,
        required=False,
        min_value=1,
        max_value=500,
        help_text="Qaytariladigan bankomatlar soni (default: 10)"
    )


class LossMakingFilterSerializer(serializers.Serializer):
    year = serializers.ChoiceField(
        choices=AVAILABLE_YEARS,
        required=False,
        allow_null=True,
        help_text="Yilni tanlang"
    )
    month = serializers.ChoiceField(
        choices=AVAILABLE_MONTHS,
        required=False,
        allow_null=True,
        help_text="Oyni tanlang"
    )
    region = serializers.ChoiceField(
        choices=AVAILABLE_REGIONS,
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="Viloyatni tanlang"
    )
    min_loss = serializers.IntegerField(
        required=False,
        default=0,
        help_text="Minimal zarar miqdori chegarasi (so'mda)"
    )
    limit = serializers.IntegerField(
        default=20,
        required=False,
        min_value=1,
        max_value=500,
        help_text="Qaytariladigan bankomatlar soni (default: 20)"
    )


class OverviewFilterSerializer(serializers.Serializer):
    year = serializers.ChoiceField(
        choices=AVAILABLE_YEARS,
        required=False,
        allow_null=True,
        help_text="Yilni tanlang (bo'sh qoldirilsa, oxirgi to'liq oy avtomatik hisoblanadi)"
    )
    month = serializers.ChoiceField(
        choices=AVAILABLE_MONTHS,
        required=False,
        allow_null=True,
        help_text="Oyni tanlang (1-12)"
    )


# =====================================================================
# RESPONSE SERIALIZERS (SWAGGER / OPENAPI SCHEMAS)
# =====================================================================

class RegionTopATMSerializer(serializers.Serializer):
    terminal_id = serializers.CharField(help_text="Terminal ID (TID)")
    name = serializers.CharField(help_text="Bankomat nomi")
    income = serializers.FloatField(help_text="Keltirgan daromadi (so'mda)")


class RegionAnalyticsItemSerializer(serializers.Serializer):
    rank = serializers.IntegerField(help_text="Reytingdagi o'rni (1, 2, ...)")
    region = serializers.CharField(help_text="Viloyat / hudud nomi")
    total_atms = serializers.IntegerField(help_text="Jami bankomatlar soni")
    active_atms = serializers.IntegerField(help_text="Faol bankomatlar soni")
    inactive_atms = serializers.IntegerField(help_text="Nofaol bankomatlar soni")
    soz_atms = serializers.IntegerField(help_text="Texnik holati SOZ bankomatlar")
    nosoz_atms = serializers.IntegerField(help_text="Texnik holati NOSOZ bankomatlar")
    uzcard_atms = serializers.IntegerField(help_text="UZCARD bankomatlar soni")
    humo_atms = serializers.IntegerField(help_text="HUMO bankomatlar soni")
    total_income = serializers.FloatField(help_text="Jami daromad (Gross income, so'mda)")
    total_cash_withdrawal = serializers.FloatField(help_text="Bankomatlardan yechilgan naqd pul aylanmasi (so'mda)")
    total_real_expense = serializers.FloatField(help_text="Jami haqiqiy xarajat: zapchast + ijara + tok + inkassatsiya + servis (so'mda)")
    maintenance_cost = serializers.FloatField(help_text="Ehtiyot qismlar va ta'mirlash xarajati (so'mda)")
    operational_cost = serializers.FloatField(help_text="Operatsion xarajatlar: ijara, tok, inkassatsiya va servis to'lovlari (so'mda)")
    net_profit = serializers.FloatField(help_text="Viloyatning sof foydasi (so'mda)")
    profit_margin = serializers.FloatField(help_text="Rentabellik marjasi (%)")
    avg_income_per_atm = serializers.FloatField(help_text="Bitta bankomatga to'g'ri keluvchi o'rtacha daromad (so'mda)")
    avg_expense_per_atm = serializers.FloatField(help_text="Bitta bankomatga to'g'ri keluvchi o'rtacha xarajat (so'mda)")
    top_atm = RegionTopATMSerializer(help_text="Ushbu viloyatdagi eng serdaromad bankomat")


class TopIncomeATMSerializer(serializers.Serializer):
    rank = serializers.IntegerField(help_text="Reytingdagi o'rni")
    atm_id = serializers.IntegerField(help_text="ATM bazaviy ID raqami")
    terminal_id = serializers.CharField(help_text="Terminal ID (TID)")
    serial_number = serializers.CharField(help_text="Bankomat seriya raqami")
    name = serializers.CharField(help_text="Bankomat nomi (BXO / BXM nomi)")
    filial_name = serializers.CharField(help_text="Filial nomi")
    region = serializers.CharField(help_text="Viloyat")
    address = serializers.CharField(help_text="Yuridik manzil")
    model = serializers.CharField(help_text="Bankomat modeli")
    card_type = serializers.CharField(help_text="Karta turi (UZCARD/HUMO)")
    status = serializers.CharField(help_text="Holati (SOZ/NOSOZ)")
    is_active = serializers.BooleanField(help_text="Faolligi")
    income = serializers.FloatField(help_text="Haqiqiy daromad (Gross revenue, so'mda)")
    cash_withdrawal = serializers.FloatField(help_text="Bankomatdan yechilgan naqd pul aylanmasi (so'mda)")
    maintenance_cost = serializers.FloatField(help_text="Zapchastlar va ta'mirlash xarajati (so'mda)")
    service_cost = serializers.FloatField(help_text="Ijara, elektr, inkassatsiya va servis xarajatlari (so'mda)")
    total_real_expense = serializers.FloatField(help_text="Jami haqiqiy xarajat (so'mda)")
    net_profit = serializers.FloatField(help_text="Sof foyda (Daromad - Jami haqiqiy xarajat, so'mda)")
    profit_margin = serializers.FloatField(help_text="Rentabellik marjasi (%)")


class TopExpenseATMSerializer(serializers.Serializer):
    rank = serializers.IntegerField(help_text="Reytingdagi o'rni")
    atm_id = serializers.IntegerField(help_text="ATM bazaviy ID raqami")
    terminal_id = serializers.CharField(help_text="Terminal ID (TID)")
    serial_number = serializers.CharField(help_text="Bankomat seriya raqami")
    name = serializers.CharField(help_text="Bankomat nomi (BXO / BXM)")
    filial_name = serializers.CharField(help_text="Filial nomi")
    region = serializers.CharField(help_text="Viloyat")
    address = serializers.CharField(help_text="Yuridik manzil")
    model = serializers.CharField(help_text="Bankomat modeli")
    card_type = serializers.CharField(help_text="Karta turi")
    status = serializers.CharField(help_text="Holati (SOZ/NOSOZ)")
    income = serializers.FloatField(help_text="Keltirgan daromadi (so'mda)")
    cash_withdrawal = serializers.FloatField(help_text="Yechilgan naqd pul aylanmasi (so'mda)")
    maintenance_cost = serializers.FloatField(help_text="Zapchast va ta'mirlash xarajati (so'mda)")
    rent_cost = serializers.FloatField(help_text="Ijara (arenda) xarajati (so'mda)")
    electricity_cost = serializers.FloatField(help_text="Elektr (tok) xarajati (so'mda)")
    incassation_cost = serializers.FloatField(help_text="Inkassatsiya xarajati (so'mda)")
    service_fees = serializers.FloatField(help_text="BTech va Glob shartnoma to'lovlari (so'mda)")
    total_real_expense = serializers.FloatField(help_text="Jami haqiqiy xarajat (so'mda)")
    net_profit = serializers.FloatField(help_text="Sof natija (Daromad - Xarajat, so'mda)")
    expense_to_income_ratio = serializers.FloatField(help_text="Xarajatning daromadga nisbati (%)")
    repairs_count = serializers.IntegerField(help_text="O'tkazilgan ta'mirlashlar soni")


class LossMakingATMSerializer(serializers.Serializer):
    rank = serializers.IntegerField(help_text="Reytingdagi o'rni")
    atm_id = serializers.IntegerField(help_text="ATM bazaviy ID raqami")
    terminal_id = serializers.CharField(help_text="Terminal ID (TID)")
    serial_number = serializers.CharField(help_text="Bankomat seriya raqami")
    name = serializers.CharField(help_text="Bankomat nomi (BXO / BXM)")
    filial_name = serializers.CharField(help_text="Filial nomi")
    region = serializers.CharField(help_text="Viloyat")
    address = serializers.CharField(help_text="Yuridik manzil")
    model = serializers.CharField(help_text="Bankomat modeli")
    card_type = serializers.CharField(help_text="Karta turi")
    status = serializers.CharField(help_text="Holati (SOZ/NOSOZ)")
    income = serializers.FloatField(help_text="Keltirgan daromadi (so'mda)")
    cash_withdrawal = serializers.FloatField(help_text="Yechilgan naqd pul aylanmasi (so'mda)")
    total_real_expense = serializers.FloatField(help_text="Jami haqiqiy xarajat (so'mda)")
    loss_amount = serializers.FloatField(help_text="Ko'rilayotgan zarar miqdori (so'mda)")
    maintenance_cost = serializers.FloatField(help_text="Ta'mirlash va zapchast xarajati (so'mda)")
    rent_cost = serializers.FloatField(help_text="Ijara to'lovi (so'mda)")
    operational_cost = serializers.FloatField(help_text="Tok, inkassatsiya va servis xarajatlari (so'mda)")
    primary_cause = serializers.CharField(help_text="Zararning asosiy sababi kodi")
    action_required = serializers.CharField(help_text="Talab etiladigan amaliy harakat: JOYINI_ALMASHTIRISH, TEXNIK_AUDIT_YOKI_YANGILASH, IJARA_MUZOKARASI_YOKI_KOCHIRISH")
    urgency_level = serializers.CharField(help_text="Shoshilinchlik darajasi: YUQORI, O'RTA, PAST")
    recommendation = serializers.CharField(help_text="Bazadagi real raqamlarga asoslangan aqlli amaliy tavsiya matni")


class OverviewKPIItemSerializer(serializers.Serializer):
    total_income = serializers.FloatField(help_text="Tarmoqning jami daromadi (so'mda)")
    total_cash_withdrawal = serializers.FloatField(help_text="Bankomatlardan yechilgan jami naqd pul aylanmasi (so'mda)")
    total_real_expense = serializers.FloatField(help_text="Tarmoqning jami haqiqiy xarajati (so'mda)")
    total_maintenance_cost = serializers.FloatField(help_text="Jami ehtiyot qismlar va ta'mirlash xarajati (so'mda)")
    total_rent_cost = serializers.FloatField(help_text="Jami ijara (arenda) xarajati (so'mda)")
    total_operational_cost = serializers.FloatField(help_text="Jami tok, inkassatsiya va servis to'lovlari (so'mda)")
    total_net_profit = serializers.FloatField(help_text="Tarmoqning jami sof foydasi (so'mda)")
    overall_profit_margin = serializers.FloatField(help_text="Tarmoq rentabellik marjasi (%)")
    total_atms = serializers.IntegerField(help_text="Jami bankomatlar soni")
    active_atms = serializers.IntegerField(help_text="Faol bankomatlar soni")
    loss_making_atms_count = serializers.IntegerField(help_text="Zararda ishlayotgan bankomatlar soni")
    relocation_recommended_count = serializers.IntegerField(help_text="Joyini almashtirish (relokatsiya) tavsiya etilgan bankomatlar soni")


class OverviewLeaderRegionSerializer(serializers.Serializer):
    region = serializers.CharField(allow_null=True)
    total_income = serializers.FloatField(required=False)
    total_real_expense = serializers.FloatField(required=False)
    net_profit = serializers.FloatField()
    total_atms = serializers.IntegerField()


class OverviewLeaderATMSerializer(serializers.Serializer):
    terminal_id = serializers.CharField(allow_null=True)
    name = serializers.CharField(allow_null=True)
    region = serializers.CharField(allow_null=True)
    income = serializers.FloatField(required=False)
    cash_withdrawal = serializers.FloatField(required=False)
    total_real_expense = serializers.FloatField(required=False)
    maintenance_cost = serializers.FloatField(required=False)
    net_profit = serializers.FloatField(required=False)


class ManagementOverviewResponseSerializer(serializers.Serializer):
    period_label = serializers.CharField(help_text="Tahlil davri (masalan: 2026-yil Iyun (O'tgan oy))")
    year = serializers.IntegerField(allow_null=True)
    month = serializers.IntegerField(allow_null=True)
    kpi_overview = OverviewKPIItemSerializer()
    top_revenue_atm = OverviewLeaderATMSerializer(allow_null=True)
    top_expense_atm = OverviewLeaderATMSerializer(allow_null=True)
    top_profit_region = OverviewLeaderRegionSerializer(allow_null=True)
    most_problematic_region = OverviewLeaderRegionSerializer(allow_null=True)
