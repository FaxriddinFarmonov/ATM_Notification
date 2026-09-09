from django.urls import path

from apps.Bankomat_hisobot.services.region_ai_analysis import RegionAIAnalysisAPIView

urlpatterns = [
    path(
        "regions/ai-analysis/",
        RegionAIAnalysisAPIView.as_view(),
        name="v2-region-ai-analysis",
    ),
]
