# reader.py
import pandas as pd


import os


class ExcelReader:

    def read(self, path):

        if not os.path.exists(path):
            raise FileNotFoundError(f"Excel file not found: {path}")

        import pandas as pd

        df = pd.read_excel(path, dtype=str)
        df = df.fillna("")
        return df.to_dict("records")