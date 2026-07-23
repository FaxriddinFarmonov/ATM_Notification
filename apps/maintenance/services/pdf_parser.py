import logging
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
import pdfplumber
from django.db import transaction
from ..models import DocumentUpload, MaintenanceProtocol, MaintenanceItem
from .link_maintenance import link_maintenance_items
from django.db import transaction

from ..models import (
    DocumentUpload,
    MaintenanceProtocol,
    MaintenanceItem,
)


logger = logging.getLogger(__name__)


class PDFProtocolParserService:
    AKT_COL_COUNT = 11
    @classmethod
    def clean_decimal(cls, val):
        if not val:
            return Decimal('0.00')
        cleaned = re.sub(r'[^\d.,-]', '', str(val).strip()).replace(' ', '')
        if ',' in cleaned and '.' in cleaned:
            cleaned = cleaned.replace(',', '')
        elif ',' in cleaned:
            cleaned = cleaned.replace(',', '.')
        try:
            return Decimal(cleaned)
        except InvalidOperation:
            return Decimal('0.00')

    @classmethod
    def clean_text(cls, val):
        if val is None:
            return ""
        return re.sub(r'\s+', ' ', str(val)).strip()

    @classmethod
    def extract_metadata(cls, text):
        universal_date_pattern = r'\b(\d{2})\s*\.\s*(\d{2})\s*\.\s*(\d{4})\b'
        date_match = re.search(universal_date_pattern, text)
        parsed_date = datetime.now().date()

        if date_match:
            day, month, year = date_match.groups()
            try:
                parsed_date = datetime.strptime(f"{day}.{month}.{year}", "%d.%m.%Y").date()
            except ValueError:
                pass

        return {
            'protocol_number': "BRP-" + parsed_date.strftime("%Y%m%d"),
            'protocol_date': parsed_date
        }

    @classmethod
    def _is_akt_header_row(cls, row):
        if not row or len(row) < 3:
            return False
        col1 = cls.clean_text(row[1]).lower()
        col2 = cls.clean_text(row[2]).lower()
        return "модул" in col1 and "серийн" in col2

    @classmethod
    def _is_akt_data_row(cls, row):
        if not row or len(row) < cls.AKT_COL_COUNT:
            return False
        first = cls.clean_text(row[0])
        return first.isdigit()

    @classmethod
    def extract_akt_rows(cls, pdf):
        akt_rows = []
        collecting = False
        expected_next = 1

        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:
                    if not collecting:
                        if cls._is_akt_header_row(row):
                            collecting = True
                        continue

                    if cls._is_akt_data_row(row):
                        row_num = int(cls.clean_text(row[0]))
                        if row_num == expected_next:
                            akt_rows.append(row)
                            expected_next += 1
                            continue
                        collecting = False
                        break
                    else:
                        collecting = False
                        break

        return akt_rows

    @classmethod
    def parse_document(cls, document_id):
        try:
            doc_instance = DocumentUpload.objects.get(pk=document_id)
        except DocumentUpload.DoesNotExist:
            logger.error(f"Hujjat topilmadi: ID {document_id}")
            return

        try:
            with pdfplumber.open(doc_instance.file.path) as pdf:
                full_text = "\n".join((page.extract_text() or "") for page in pdf.pages)
                akt_rows = cls.extract_akt_rows(pdf)

                if not akt_rows:
                    logger.warning(
                        f"Hujjat ID {document_id}: 'AKT' jadvali topilmadi, hech narsa saqlanmadi."
                    )
                    return

                metadata = cls.extract_metadata(full_text)

                with transaction.atomic():
                    MaintenanceItem.objects.filter(document=doc_instance).delete()
                    MaintenanceProtocol.objects.filter(document_source=doc_instance).delete()

                    protocol = MaintenanceProtocol.objects.create(
                        document_source=doc_instance,
                        protocol_number=metadata['protocol_number'],
                        protocol_date=metadata['protocol_date']
                    )

                    for row in akt_rows:
                        row_num_val = int(cls.clean_text(row[0]))
                        equipment_module = cls.clean_text(row[1])
                        serial_number = cls.clean_text(row[2])
                        part_name = cls.clean_text(row[3]) or "N/A"

                        qty = cls.clean_decimal(row[4])
                        price = cls.clean_decimal(row[5])
                        total = cls.clean_decimal(row[6])
                        vat_amt = cls.clean_decimal(row[7])
                        total_with_vat = cls.clean_decimal(row[8])

                        filial_name = cls.clean_text(row[9])
                        mfo_bank = cls.clean_text(row[10])

                        MaintenanceItem.objects.create(
                            document=doc_instance,
                            protocol=protocol,
                            protocol_date=metadata['protocol_date'],
                            row_number=row_num_val,
                            equipment_module=equipment_module,
                            serial_number=serial_number,
                            part_name=part_name,
                            quantity=qty,
                            price_per_unit=price,
                            total_amount=total,
                            vat_amount=vat_amt,
                            total_with_vat=total_with_vat,
                            filial_name=filial_name,
                            mfo_bank=mfo_bank,
                        )

                doc_instance.is_processed = True
                doc_instance.save(update_fields=["is_processed"])

                # ATMTechnical bilan bog'lash
                linked = link_maintenance_items()

                logger.info(
                    f"""
                    Hujjat muvaffaqiyatli parsalandi.

                    Document ID : {doc_instance.id}

                    Rows        : {len(akt_rows)}

                    Linked ATM  : {linked}
                    """
                )

        except Exception as e:
            logger.exception(f"Parsing jarayonida xatolik: {str(e)}")