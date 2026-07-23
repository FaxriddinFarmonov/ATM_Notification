from django.db import transaction

from .reader import ExcelReader
from .header_extractor import HeaderExtractor
from .schema_builder import SchemaBuilder
from .row_parser import RowParser

from .savers.contract_saver import ContractSaver
from .savers.payment_saver import PaymentSaver


class ExcelImporter:

    def __init__(self, file_path):
        self.file_path = file_path

    @transaction.atomic
    def run(self):

        sheet = ExcelReader(
            self.file_path,
        ).open()

        headers = HeaderExtractor.extract(
            sheet,
        )

        schema = SchemaBuilder.build(
            headers,
        )

        imported = 0
        skipped = 0

        for values in sheet.iter_rows(
            min_row=3,
            values_only=True,
        ):

            parsed = RowParser.parse(
                schema=schema,
                values=values,
            )

            if not parsed.terminal_id:
                print("Terminal ID yo'q:", parsed)
                skipped += 1
                continue

            if self.save(parsed):
                imported += 1
            else:
                print("ATM topilmadi:", parsed.terminal_id)
                skipped += 1

        return {
            "imported": imported,
            "skipped": skipped,
        }

    def save(self, parsed):

        contract = ContractSaver.save(parsed)

        if contract is None:
            return False

        PaymentSaver.save_services(
            contract=contract,
            parsed=parsed,
        )

        PaymentSaver.save_payments(
            contract=contract,
            parsed=parsed,
        )

        return True