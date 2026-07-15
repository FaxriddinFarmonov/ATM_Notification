
from rest_framework import serializers

from apps.Bankomat_hisobot.models.full_models import ATMTechnical



class ATMFilterSerializer(serializers.Serializer):

    status = serializers.ChoiceField(
        choices=ATMTechnical.STATUS_CHOICES,
        required=False,
    )

    card_type = serializers.ChoiceField(
        choices=ATMTechnical.CARD_CHOICES,
        required=False,
    )

    region = serializers.CharField(
        required=False,
    )

    model = serializers.CharField(
        required=False,
    )

    is_active = serializers.BooleanField(
        required=False,
        default=serializers.empty,
    )