import os
import sys
import django
import pandas as pd
from django.db import transaction

# Setup Django environment
sys.path.append(r'd:\PycharmProjects\Bankomat_Notification_bot')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import Engineer
from apps.atms.models import ATM

excel_path = r'C:\Users\Faxriddin\Downloads\Bankomat GLOBE.xlsx'

if not os.path.exists(excel_path):
    print(f"File not found: {excel_path}")
    sys.exit(1)

# Delete existing engineers so clean import runs
Engineer.objects.all().delete()

df = pd.read_excel(excel_path, dtype=str)
df = df.fillna("")

created_engineers = 0
assigned_atms = 0

def clean_str(val):
    if not val or pd.isna(val):
        return ""
    s = str(val).strip()
    s = s.replace("\xa0", " ").strip()
    return s

with transaction.atomic():
    for idx, row in df.iterrows():
        fio = clean_str(row.get("F.I.O"))
        phone = clean_str(row.get("TEL nomer"))
        tg_id = clean_str(row.get("Telegram  id"))
        serial = clean_str(row.get("Serial number"))
        tid = clean_str(row.get("TerminalID")) or clean_str(row.get("TID"))
        address = clean_str(row.get("Address"))
        model_name = clean_str(row.get("Model"))
        merchant_id = clean_str(row.get("MerchantID"))
        mfo = clean_str(row.get("MFO"))

        if not fio:
            continue

        # Split name into first, last, patronymic
        parts = fio.split()
        first_name = parts[1] if len(parts) > 1 else (parts[0] if parts else "")
        last_name = parts[0] if parts else ""
        patronymic = " ".join(parts[2:]) if len(parts) > 2 else ""

        # Find or create Engineer
        engineer = None
        if tg_id:
            engineer = Engineer.objects.filter(telegram_chat_id=tg_id).first()
        if not engineer and phone:
            engineer = Engineer.objects.filter(phone=phone).first()
        if not engineer and fio:
            engineer = Engineer.objects.filter(full_name=fio).first()

        if not engineer:
            engineer = Engineer.objects.create(
                first_name=first_name,
                last_name=last_name,
                patronymic=patronymic,
                full_name=fio,
                phone=phone,
                telegram_chat_id=tg_id,
                is_active=True,
                specialization="ATM Servis Muhandisi"
            )
            created_engineers += 1
        else:
            engineer.full_name = fio
            if phone and not engineer.phone:
                engineer.phone = phone
            if tg_id and not engineer.telegram_chat_id:
                engineer.telegram_chat_id = tg_id
            if first_name and not engineer.first_name:
                engineer.first_name = first_name
            if last_name and not engineer.last_name:
                engineer.last_name = last_name
            engineer.is_active = True
            engineer.save()

        # Match and Assign ATM
        atm = None
        if serial:
            atm = ATM.objects.filter(serial=serial).first()
        if not atm and tid:
            atm = ATM.objects.filter(tid=tid).first()

        if not atm and serial:
            atm = ATM.objects.create(
                external_id=abs(hash(serial)) % 1000000000,
                serial=serial,
                tid=tid,
                address=address,
                model_name=model_name,
                extra_attrs={"mfo": mfo, "merchantId": merchant_id, "terminalId": tid}
            )

        if atm:
            atm.responsible_engineer = engineer
            if address and not atm.address:
                atm.address = address
            if model_name and not atm.model_name:
                atm.model_name = model_name
            atm.save(update_fields=["responsible_engineer", "address", "model_name"])
            assigned_atms += 1

print(f"PERFECT CLEAN IMPORT COMPLETED SUCCESSFULLY:")
print(f"Created Engineers: {created_engineers}")
print(f"Assigned ATMs: {assigned_atms}")

print("\nFINAL SUMMARY OF ENGINEERS & ASSIGNED ATM COUNTS:")
for eng in Engineer.objects.filter(is_active=True).order_by("full_name"):
    count = eng.assigned_atms.count()
    print(f"- {eng.full_name} | Tel: {eng.phone or '---'} | TG: {eng.telegram_chat_id or '---'} | Biriktirilgan ATM: {count} ta")
