# normalizer.py


class ExcelNormalizer:

    def normalize(self, row: dict):

        return {
            "serial": str(row.get("Serial number", "")).strip(),
            "tid": str(row.get("TID", "")).strip(),
            "telegram_chat_id": str(row.get("Telegram  id", "")).strip(),
            "merchant_id": str(row.get("MerchantID", "")).strip(),

            "fio": str(row.get("F.I.O", "")).strip(),
            "phone": str(row.get("TEL nomer", "")).strip(),
            "telegram_id": str(row.get("Telegram  id", "")).strip(),
        }