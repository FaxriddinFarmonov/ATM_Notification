import requests
from apps.atms.models import BTechConfig
from apps.monitoring.models import MonitoringConfig


class MonitoringClient:

    def get_atms(self):
        btech_config = BTechConfig.objects.filter(is_active=True).first()

        if btech_config:
            token = btech_config.bearer_token.strip()
            api_url = btech_config.api_url.strip()
        else:
            config = MonitoringConfig.objects.first()
            if not config:
                btech_config = BTechConfig.objects.create()
                token = btech_config.bearer_token.strip()
                api_url = btech_config.api_url.strip()
            else:
                token = config.bearer_token.strip()
                api_url = config.api_url.strip()

        if not token.startswith("Bearer "):
            auth_header = f"Bearer {token}"
        else:
            auth_header = token

        headers = {
            "Authorization": auth_header,
            "Accept": "application/json"
        }

        response = requests.get(
            api_url,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()
        return response.json()