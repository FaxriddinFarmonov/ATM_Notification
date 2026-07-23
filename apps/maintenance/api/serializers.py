from rest_framework import serializers
from ..models import DocumentUpload, MaintenanceProtocol, MaintenanceItem


class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentUpload
        fields = ['id', 'title', 'file', 'uploaded_at', 'is_processed']
        read_only_fields = ['is_processed', 'uploaded_at']


class MaintenanceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceItem
        fields = '__all__'


class MaintenanceProtocolSerializer(serializers.ModelSerializer):
    items = MaintenanceItemSerializer(many=True, read_only=True)
    items_count = serializers.IntegerField(source='items.count', read_only=True)

    class Meta:
        model = MaintenanceProtocol
        fields = [
            'id', 'document_source', 'protocol_number', 'protocol_date', 
            'performer_company', 'customer_bank', 'items_count', 'items'
        ]