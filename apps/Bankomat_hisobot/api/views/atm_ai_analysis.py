from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from ...services.atm_detail_queryset import ATMDetailQuerySet
from ...services.atm_analytics import ATMAnalyticsService
from ...services.prompt_builder import PromptBuilder
from ...services.ollama_service import OllamaService


@extend_schema(
    tags=["ATM AI"],
    summary="ATM AI Analysis",
    description="Returns AI generated analysis for a single ATM.",
)
class ATMAIAnalysisAPIView(APIView):

    def post(self, request, pk):

        atm = ATMDetailQuerySet.get(pk)

        analytics = ATMAnalyticsService(
            atm
        ).build()

        prompt = PromptBuilder.build(
            analytics
        )

        analysis = OllamaService.generate(
            prompt
        )

        return Response({

            "analysis": analysis,

        })