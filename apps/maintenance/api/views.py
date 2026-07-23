from rest_framework import viewsets, parsers
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import DocumentUpload, MaintenanceProtocol, MaintenanceItem
from .serializers import (
    DocumentUploadSerializer, 
    MaintenanceProtocolSerializer, 
    MaintenanceItemSerializer
)


class DocumentUploadViewSet(viewsets.ModelViewSet):
    queryset = DocumentUpload.objects.all()
    serializer_class = DocumentUploadSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_processed']
    ordering_fields = ['uploaded_at']


class MaintenanceProtocolViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceProtocol.objects.all().prefetch_related('items').select_related('document_source')
    serializer_class = MaintenanceProtocolSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['protocol_date', 'performer_company']
    search_fields = ['protocol_number', 'performer_company', 'customer_bank']
    ordering_fields = ['protocol_date', 'protocol_number']


class MaintenanceItemViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceItem.objects.all().select_related('protocol')
    serializer_class = MaintenanceItemSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['protocol']
    search_fields = ['part_name']
    ordering_fields = ['row_number', 'total_with_vat']