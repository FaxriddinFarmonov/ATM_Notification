from .excel_styles import ExcelStyles


class SheetBuilder:

    def __init__(self, workbook):

        self.workbook = workbook

    def create(self, title):

        sheet = self.workbook.active

        sheet.title = title

        sheet.freeze_panes = "A5"

        return sheet

    def title(self, sheet, text):

        cell = sheet["A1"]

        cell.value = text

        cell.font = ExcelStyles.TITLE_FONT