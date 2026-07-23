from rest_framework.routers import DefaultRouter
from .views import (
    DocumentUploadViewSet, 
    MaintenanceProtocolViewSet, 
    MaintenanceItemViewSet
)

router = DefaultRouter()
router.register(r'api/v1/uploads', DocumentUploadViewSet, basename='upload')
router.register(r'api/v1/protocols', MaintenanceProtocolViewSet, basename='protocol')
router.register(r'api/v1/items', MaintenanceItemViewSet, basename='item')

urlpatterns = router.urls