from rest_framework import serializers

from ...services.atm_business import ATMBusinessService


class ATMGeneralInfoSerializer(serializers.Serializer):
    region = serializers.CharField()
    name = serializers.CharField()
    address = serializers.CharField()
    card_type = serializers.CharField()
    model = serializers.CharField()


class ATMTechnicalInfoSerializer(serializers.Serializer):
    merchant_id = serializers.CharField(allow_blank=True)
    terminal_id = serializers.CharField()
    status = serializers.CharField()
    serial_number = serializers.CharField(allow_blank=True)
    inventory_number = serializers.CharField(allow_blank=True)
    account_23510 = serializers.CharField(allow_blank=True)
    account_45265 = serializers.CharField(allow_blank=True)


class ATMServicePaymentItemSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    payment_type = serializers.CharField()
    amount = serializers.FloatField()


class ATMServiceContractInfoSerializer(serializers.Serializer):
    btech_monthly_fee = serializers.FloatField()
    glob_monthly_fee = serializers.FloatField()
    payments = ATMServicePaymentItemSerializer(many=True)


class ATMMonthlyStatisticItemSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    income = serializers.FloatField()
    expense = serializers.FloatField()
    repair_cost = serializers.FloatField()
    quantity = serializers.FloatField()


class ATMYearlyStatisticItemSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    card_type = serializers.CharField()
    income = serializers.FloatField()
    expense = serializers.FloatField()
    repair_cost = serializers.FloatField()
    quantity = serializers.FloatField()


class ATMDetailSerializer(serializers.Serializer):
    general = ATMGeneralInfoSerializer()
    technical = ATMTechnicalInfoSerializer()
    service_contract = ATMServiceContractInfoSerializer(allow_null=True)
    monthly_statistics = ATMMonthlyStatisticItemSerializer(many=True)
    yearly_statistics = ATMYearlyStatisticItemSerializer(many=True)

    def to_representation(self, instance):
        service = ATMBusinessService(instance)
        return service.build()