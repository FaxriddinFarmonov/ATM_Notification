import requests

from django.conf import settings

import requests

from apps.monitoring.models import MonitoringConfig


class MonitoringClient:

    def get_atms(self):

        config = MonitoringConfig.objects.first()

        if not config:
            raise Exception("MonitoringConfig topilmadi")

        headers = {
            "Authorization": config.bearer_token
        }

        response = requests.get(
            config.api_url,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        return response.json()