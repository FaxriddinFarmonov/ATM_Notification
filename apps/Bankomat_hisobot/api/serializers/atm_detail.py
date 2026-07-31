from rest_framework import serializers

from ...services.atm_business import ATMBusinessService


class ATMDetailSerializer(serializers.Serializer):

    def to_representation(self, instance):

        service = ATMBusinessService(instance)

        return service.build()