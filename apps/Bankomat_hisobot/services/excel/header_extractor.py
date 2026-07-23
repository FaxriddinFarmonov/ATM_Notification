from typing import List


class HeaderExtractor:

    HEADER_ROW_1 = 1
    HEADER_ROW_2 = 2

    @classmethod
    def extract(cls, sheet) -> List[str]:

        first = [
            cell.value
            for cell in sheet[cls.HEADER_ROW_1]
        ]

        second = [
            cell.value
            for cell in sheet[cls.HEADER_ROW_2]
        ]

        headers = []

        last_title = ""

        for h1, h2 in zip(first, second):

            if h1:

                last_title = str(h1).strip()

            title = last_title

            if h2:

                title += " | " + str(h2).strip()

            headers.append(title)

        return headers