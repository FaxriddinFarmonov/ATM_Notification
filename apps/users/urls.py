from django.urls import path
from apps.users.views import (
    EngineerListCreateAPIView,
    EngineerDetailAPIView,
    AssignAtmAPIView,
    UnassignAtmAPIView,
    AvailableATMsAPIView,
    AtmEngineerAPIView,
    BTechTokenAPIView,
    BTechSyncAPIView,
)

urlpatterns = [
    path("engineers/", EngineerListCreateAPIView.as_view(), name="engineer-list-create"),
    path("engineers/<int:pk>/", EngineerDetailAPIView.as_view(), name="engineer-detail"),
    path("engineers/<int:pk>/assign-atm/", AssignAtmAPIView.as_view(), name="engineer-assign-atm"),
    path("engineers/<int:pk>/unassign-atm/", UnassignAtmAPIView.as_view(), name="engineer-unassign-atm"),
    path("engineers/atms/available/", AvailableATMsAPIView.as_view(), name="available-atms"),
    path("engineers/atm/<str:serial>/engineer/", AtmEngineerAPIView.as_view(), name="atm-engineer"),
    path("btech/token/", BTechTokenAPIView.as_view(), name="btech-token"),
    path("btech/sync/", BTechSyncAPIView.as_view(), name="btech-sync"),
]
