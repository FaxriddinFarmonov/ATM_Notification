from django.urls import path

from .views.atm_ai_analysis import ATMAIAnalysisAPIView
from .views.atm_filter_options import ATMFilterOptionsAPIView
from .views.full_exel_export import ATMExcelExportAPIView, FullATMExcelExportAPIView
from .views.maintenance import (
    MaintenanceListAPIView,
    MaintenanceDetailAPIView,
)
from .views.atm_detail import ATMDetailAPIView
from .views.atm_list import ATMListAPIView
from .views.dashboard import DashboardAPIView
from .views.maintenance import MaintenanceListAPIView

urlpatterns = [
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
        "dashboard/",
        DashboardAPIView.as_view(),
        name="dashboard",
    ),

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

    path(
        "atms/<str:pk>/ai-analysis/",
        ATMAIAnalysisAPIView.as_view(),
    ),
    path(
        "atms/<str:pk>/export/",
        ATMExcelExportAPIView.as_view(),
        name="atm-export",
    ),



]