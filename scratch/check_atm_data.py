import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.Bankomat_hisobot.models.full_models import ATMTURON
from apps.Bankomat_hisobot.services.atm_business import ATMBusinessService
from apps.Bankomat_hisobot.models.ATMServiceContract import ATMServiceContract, ATMServicePayment

atms = ATMTURON.objects.all()[:5]
print(f"Total ATMs found: {atms.count()}")

for atm in atms:
    service = ATMBusinessService(atm)
    data = service.build()
    print(f"\n--- ATM {atm.terminal_id} ({atm.region}) ---")
    print("General:", data.get('general'))
    print("Service contract:", data.get('service_contract'))
    stats = data.get('monthly_statistics', [])
    print(f"Monthly stats count: {len(stats)}")
    if stats:
        print("Sample month stat (latest):", stats[-1])

contracts_count = ATMServiceContract.objects.count()
payments_count = ATMServicePayment.objects.count()
print(f"\nTotal Service Contracts in DB: {contracts_count}")
print(f"Total Payments in DB: {payments_count}")
