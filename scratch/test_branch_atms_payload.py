import os
import sys
import django
import json

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.Bankomat_hisobot.services.analytics_service import TopIncomeATMsService
from apps.Bankomat_hisobot.services.atm_business import ATMBusinessService
from apps.Bankomat_hisobot.models.full_models import ATMTURON

# 1. Check TopIncomeATMsService results for region Navoiy
navoiy_items = TopIncomeATMsService.get(region="Navoiy", limit=10)
print(f"Top income items count for Navoiy: {len(navoiy_items)}")
if navoiy_items:
    print("First item keys & values:")
    print(json.dumps(navoiy_items[0], indent=2, default=str))

# 2. Check if ATMTURON lookup works by terminal_id vs pk
sample_tid = navoiy_items[0]['terminal_id'] if navoiy_items else '15896'
print(f"\nTesting ATMTURON lookup for TID: {sample_tid}")
try:
    atm_obj = ATMTURON.objects.get(terminal_id=sample_tid)
    print(f"Found ATMTURON by terminal_id! PK = {atm_obj.pk}, terminal_id = {atm_obj.terminal_id}, region = {atm_obj.region}")
    service = ATMBusinessService(atm_obj)
    detail = service.build()
    print("Build keys:", detail.keys())
    print("General:", detail.get('general'))
except Exception as e:
    print(f"Error looking up ATMTURON: {e}")
