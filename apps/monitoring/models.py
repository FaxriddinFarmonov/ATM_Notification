from django.db import models

# Create your models here.
from django.db import models


class MonitoringConfig(models.Model):
    api_url = models.TextField()
    bearer_token = models.TextField()

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Monitoring API Config"


# MONITORING_API_URL = "https://monitoring.btech.uz/api/base/atm/?clientId=&vendorId=&modelId=&functionId=&variantId=&atmGroupId=&countryId=&regionId=&cityId=&hashTags=&appConnectionStatus=all&agentConnectionStatus=online&hwFaults=&atmStatus=all&withUnitsTurnoverTotal=true&offset=0&limit=500&lang=en"
#
# MONITORING_API_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjM2NiwiaWF0IjoxNzgyMTE2ODUyLCJleHAiOjE3ODIzNzYwNTJ9.UqQQUZaIYkosLH3w9Z3kb6fB-PnS1dR5e1rHenYwyGQ"
# # Default primary key field type