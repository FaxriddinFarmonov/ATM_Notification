from django.urls import path
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
        "atms/",
        ATMListAPIView.as_view(),
        name="atm-list",
    ),
    path(
            "atms/<int:pk>/",
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
        "maintenance/",
        MaintenanceListAPIView.as_view(),
        name="maintenance-list",
    ),

    path(
        "maintenance/<int:pk>/",
        MaintenanceDetailAPIView.as_view(),
        name="maintenance-detail",
    ),
    
    ]