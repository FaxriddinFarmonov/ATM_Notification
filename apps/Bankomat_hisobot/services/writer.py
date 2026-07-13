from openpyxl import Workbook


class WorkbookWriter:

    def create_workbook(self):

        workbook = Workbook()

        workbook.properties.creator = "Turonbank"

        workbook.properties.company = "Turonbank"

        workbook.properties.title = "ATM Report"

        workbook.properties.subject = "ATM Statistics"

        workbook.properties.category = "Reports"

        workbook.properties.description = (
            "ATM statistics export"
        )

        return workbook