from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.Bankomat_hisobot.services.region_analytics import (
    RegionAnalyticsService,
)

from apps.Bankomat_hisobot.services.region_prompt_builder import (
    RegionPromptBuilder,
)

from apps.Bankomat_hisobot.services.region_ollama_service import (
    RegionOllamaService,
)


from rest_framework import serializers
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import OpenApiExample

from apps.Bankomat_hisobot.api.swagger_constants import (
    AVAILABLE_REGIONS,
    AVAILABLE_YEARS,
    AVAILABLE_MONTHS,
)

class RegionAIAnalysisRequestSerializer(serializers.Serializer):
    region = serializers.ChoiceField(
        choices=AVAILABLE_REGIONS,
        required=True,
        help_text="Tahlil qilinadigan viloyatni tanlang"
    )
    start_year = serializers.ChoiceField(
        choices=AVAILABLE_YEARS,
        required=False,
        allow_null=True,
        help_text="Boshlang'ich yilni tanlang"
    )
    end_year = serializers.ChoiceField(
        choices=AVAILABLE_YEARS,
        required=False,
        allow_null=True,
        help_text="Tugash yilini tanlang"
    )
    start_month = serializers.ChoiceField(
        choices=AVAILABLE_MONTHS,
        required=False,
        allow_null=True,
        help_text="Boshlang'ich oyni tanlang (1-12)"
    )
    end_month = serializers.ChoiceField(
        choices=AVAILABLE_MONTHS,
        required=False,
        allow_null=True,
        help_text="Tugash oyini tanlang (1-12)"
    )


class RegionAIAnalysisResponseSerializer(serializers.Serializer):
    region = serializers.CharField()
    start_year = serializers.IntegerField(allow_null=True)
    end_year = serializers.IntegerField(allow_null=True)
    start_month = serializers.IntegerField(allow_null=True)
    end_month = serializers.IntegerField(allow_null=True)
    analytics = serializers.DictField(help_text="Viloyatning hisoblangan statistikasi")
    analysis = serializers.CharField(help_text="Ollama AI matnli tahliliy xulosasi")


@extend_schema(
    tags=["ATM AI"],
    summary="Viloyat bo'yicha Ollama AI tahlili",
    description="Tanlangan viloyatning oylar va yillar kesimidagi statistikasi asosida Ollama LLM orqali tahlil va tavsiyalar olish.",
    request=RegionAIAnalysisRequestSerializer,
    responses={200: RegionAIAnalysisResponseSerializer},
    examples=[
        OpenApiExample(
            name="Namuna so'rov (Viloyat tahlili)",
            description="Samarqand viloyati bo'yicha 2025-yil statistikasi tahlili",
            value={
                "region": "Самарқанд",
                "start_year": 2025,
                "end_year": 2025,
                "start_month": 1,
                "end_month": 12,
            },
            request_only=True,
        )
    ],
)
class RegionAIAnalysisAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()



    def post(self, request):
        start_month = request.data.get("start_month")
        end_month = request.data.get("end_month")

        if start_month:
            start_month = int(start_month)

        if end_month:
            end_month = int(end_month)
        region = request.data.get("region")

        start_year = request.data.get("start_year")
        end_year = request.data.get("end_year")

        if not region:
            return Response(
                {
                    "error": "region majburiy."
                },
                status=400,
            )

        if start_year:
            start_year = int(start_year)

        if end_year:
            end_year = int(end_year)

        analytics = RegionAnalyticsService(
            region=region,
            start_year=start_year,
            end_year=end_year,
            start_month=start_month,
            end_month=end_month,
        ).build()
        prompt = RegionPromptBuilder.build(
            analytics
        )

        analysis = RegionOllamaService.generate(
            prompt
        )
        start_month = request.data.get("start_month")
        end_month = request.data.get("end_month")

        if start_month:
            start_month = int(start_month)

        if end_month:
            end_month = int(end_month)

        return Response(
            {
                "region": region,
                "start_year": start_year,
                "end_year": end_year,
                "start_month": start_month,
                "end_month": end_month,
                "analytics": analytics,
                "analysis": analysis,
            }
        )