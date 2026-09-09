from django.urls import path

from .views.atm_ai_analysis import ATMAIAnalysisAPIView
from apps.Bankomat_hisobot.services.region_ai_analysis import RegionAIAnalysisAPIView
from .views.atm_filter_options import ATMFilterOptionsAPIView
from .views.full_exel_export import ATMExcelExportAPIView, FullATMExcelExportAPIView
from .views.maintenance import (
    MaintenanceListAPIView,
    MaintenanceDetailAPIView,
)
from .views.atm_detail import ATMDetailAPIView
from .views.atm_list import ATMListAPIView
from .views.dashboard import DashboardAPIView
from .views.analytics import (
    YearlyComparisonAPIView,
    TopRegionsAnalyticsAPIView,
    TopIncomeATMsAPIView,
    TopExpenseATMsAPIView,
    LossMakingATMsAPIView,
    AnalyticsOverviewAPIView,
    ModelAnalyticsAPIView,
    AnnualFinancialsAPIView,
)

urlpatterns = [
    # --- ATM Base Endpoints ---
    path(
        "atms/export/",
        FullATMExcelExportAPIView.as_view(),
        name="atm-export-all",
    ),
    path(
        "atms/filters/",
        ATMFilterOptionsAPIView.as_view(),
        name="atm-filter-options",
    ),
    path(
        "atms/",
        ATMListAPIView.as_view(),
        name="atm-list",
    ),
    path(
        "atms/<str:pk>/",
        ATMDetailAPIView.as_view(),
        name="atm-detail",
    ),
    path(
        "atms/<str:pk>/ai-analysis/",
        ATMAIAnalysisAPIView.as_view(),
        name="atm-ai-analysis",
    ),
    path(
        "regions/ai-analysis/",
        RegionAIAnalysisAPIView.as_view(),
        name="region-ai-analysis",
    ),
    path(
        "atms/<str:pk>/export/",
        ATMExcelExportAPIView.as_view(),
        name="atm-export",
    ),


    # --- Dashboard ---
    path(
        "dashboard/",
        DashboardAPIView.as_view(),
        name="dashboard",
    ),

    # --- Maintenance Endpoints ---
    path(
        "maintenance/",
        MaintenanceListAPIView.as_view(),
        name="maintenance-list",
    ),
    path(
        "maintenance/<str:pk>/",
        MaintenanceDetailAPIView.as_view(),
        name="maintenance-detail",
    ),

    # --- Senior Analytics Endpoints ---
    path(
        "analytics/regions/",
        TopRegionsAnalyticsAPIView.as_view(),
        name="analytics-regions",
    ),
    path(
        "analytics/atms/top-income/",
        TopIncomeATMsAPIView.as_view(),
        name="analytics-top-income",
    ),
    path(
        "analytics/atms/top-expense/",
        TopExpenseATMsAPIView.as_view(),
        name="analytics-top-expense",
    ),
    path(
        "analytics/atms/loss-making/",
        LossMakingATMsAPIView.as_view(),
        name="analytics-loss-making",
    ),
    path(
        "analytics/overview/",
        AnalyticsOverviewAPIView.as_view(),
        name="analytics-overview",
    ),
    path(
        "analytics/models/",
        ModelAnalyticsAPIView.as_view(),
        name="analytics-models",
    ),
    path(
        "analytics/annual-financials/",
        AnnualFinancialsAPIView.as_view(),
        name="analytics-annual-financials",
    ),
    path(
        "analytics/yearly-comparison/",
        YearlyComparisonAPIView.as_view(),
        name="analytics-yearly-comparison",
    ),
]
