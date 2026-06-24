
from django.conf import settings
import requests
import requests
import time
from django.conf import settings


class TelegramSender:

    @staticmethod
    def send_message(chat_id, text):

        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

        while True:
            try:
                response = requests.post(
                    url,
                    json={
                        "chat_id": chat_id,
                        "text": text,
                        "parse_mode": "HTML"
                    },
                    timeout=30
                )

                data = response.json()

                # Telegram flood limit
                if response.status_code == 429:

                    retry_after = (
                        data.get("parameters", {})
                            .get("retry_after", 5)
                    )

                    print(f"Flood limit. Sleep {retry_after} sec")

                    time.sleep(retry_after)

                    continue

                return response.ok

            except Exception as e:
                print(e)
                return False