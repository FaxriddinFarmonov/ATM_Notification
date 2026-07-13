from openpyxl.utils import get_column_letter


def autosize_columns(sheet):

    for column in sheet.columns:

        length = 0

        column_letter = get_column_letter(
            column[0].column
        )

        for cell in column:

            try:

                if cell.value:

                    length = max(
                        length,
                        len(str(cell.value)),
                    )

            except Exception:
                pass

        sheet.column_dimensions[
            column_letter
        ].width = length + 4