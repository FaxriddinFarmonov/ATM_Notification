from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from ...services.atm_filter_options import (
    ATMFilterOptionsService,
)


from rest_framework import serializers

class FilterChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

class MonthChoiceSerializer(serializers.Serializer):
    value = serializers.IntegerField()
    label = serializers.CharField()

class BooleanChoiceSerializer(serializers.Serializer):
    value = serializers.BooleanField()
    label = serializers.CharField()

class ATMFilterOptionsResponseSerializer(serializers.Serializer):
    status = FilterChoiceSerializer(many=True)
    card_type = FilterChoiceSerializer(many=True)
    regions = serializers.ListField(child=serializers.CharField())
    models = serializers.ListField(child=serializers.CharField())
    model_names = serializers.ListField(child=serializers.CharField())
    years = serializers.ListField(child=serializers.IntegerField())
    months = MonthChoiceSerializer(many=True)
    is_active = BooleanChoiceSerializer(many=True)


@extend_schema(
    tags=["ATM"],
    summary="ATM filter options",
    description=(
        "Returns all available filter values for ATM list page. "
        "Frontend should call this endpoint once and use the "
        "returned values to populate filter dropdowns."
    ),
    responses={
        200: ATMFilterOptionsResponseSerializer
    },
)

class ATMFilterOptionsAPIView(APIView):

    permission_classes = (AllowAny,)

    authentication_classes = ()

    def get(self, request):

        return Response(
            ATMFilterOptionsService.get()
        )