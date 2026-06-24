from django.utils import timezone
import pytz


class EventMessageBuilder:

    @staticmethod
    def build(event):

        atm = event.atm
        eng = atm.responsible_engineer

        if eng:
            engineer_text = eng.full_name

            if getattr(eng, "telegram_username", None):
                engineer_text += f"\n@{eng.telegram_username}"
        else:
            engineer_text = "Not assigned"

        merchant_id = "-"
        extra = atm.extra_attrs or {}

        if isinstance(extra, dict):
            merchant_id = extra.get("merchantId", "-")

        current_time = timezone.localtime(
            timezone.now(),
            timezone=pytz.timezone("Asia/Tashkent")
        ).strftime("%Y-%m-%d %H:%M")

        return (
            f"<b>🔔 {event.event_type}</b>\n\n"
            f"🔢 Serial: {atm.serial}\n"
            f"🏧 TID: {atm.tid}\n"
            f"🏪 Merchant ID: {merchant_id}\n"
            f"📍 Joylashuv: {atm.address or '-'}\n"
            f"🏦 Model: {atm.model_name or '-'}\n\n"
            f"⚠️ Muammo:\n"
            f"{event.message}\n\n"
            f"👨‍🔧 Mas'ul texnik:\n"
            f"{engineer_text}\n\n"
            f"🕒 Vaqt:\n"
            f"{current_time}"
        )