import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.Bankomat_hisobot.services.charts import get_top_income_atms

top = get_top_income_atms(limit=5)
print("Top income ATMs structure:")
for item in top:
    print(item)
