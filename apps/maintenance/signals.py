from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DocumentUpload
from .services.pdf_parser import PDFProtocolParserService


@receiver(post_save, sender=DocumentUpload)
def trigger_pdf_processing(sender, instance, created, **kwargs):
    if created or not instance.is_processed:
        transaction.on_commit(lambda: PDFProtocolParserService.parse_document(instance.id))