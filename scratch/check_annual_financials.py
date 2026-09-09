import os
import sys
import django
from decimal import Decimal

sys.path.append(r'd:\PycharmProjects\Bankomat_Notification_bot')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.Bankomat_hisobot.models import ATMMonthlyStatistic, ATMServicePayment, ATMServiceContract
from apps.maintenance.models import MaintenanceItem
from django.db.models import Sum

def money(val):
    return float(Decimal(str(val or 0)) * 1000)

for yr in [2024, 2025, 2026]:
    inc_row = ATMMonthlyStatistic.objects.filter(year=yr).aggregate(tot=Sum('income'))
    income = money(inc_row['tot'])

    cw_row = ATMMonthlyStatistic.objects.filter(year=yr).aggregate(tot=Sum('expense'))
    cash_withdrawal = money(cw_row['tot'])

    m_row = MaintenanceItem.objects.filter(protocol_date__year=yr).aggregate(tot=Sum('total_with_vat'))
    maint_cost = float(m_row['tot'] or 0)

    rent_row = ATMServicePayment.objects.filter(year=yr, payment_type='RENT').aggregate(tot=Sum('amount'))
    rent_cost = money(rent_row['tot'])

    elec_row = ATMServicePayment.objects.filter(year=yr, payment_type='ELECTRICITY').aggregate(tot=Sum('amount'))
    elec_cost = money(elec_row['tot'])

    incass_row = ATMServicePayment.objects.filter(year=yr, payment_type='INCASSATION').aggregate(tot=Sum('amount'))
    incass_cost = money(incass_row['tot'])

    months_count = 12 if yr in [2024, 2025] else 6
    contract_row = ATMServiceContract.objects.aggregate(
        btech=Sum('btech_monthly_fee'),
        glob=Sum('glob_monthly_fee')
    )
    btech_cost = money(contract_row['btech']) * months_count
    glob_cost = money(contract_row['glob']) * months_count

    total_expense = maint_cost + rent_cost + elec_cost + incass_cost + btech_cost + glob_cost
    net_profit = income - total_expense
    margin = (net_profit / income * 100) if income > 0 else 0.0

    print(f"=== YEAR {yr} ===")
    print(f"Income: {income:,.2f} UZS")
    print(f"Cash Withdrawal: {cash_withdrawal:,.2f} UZS")
    print(f"Maintenance (Zapchast): {maint_cost:,.2f} UZS")
    print(f"Rent (Ijara): {rent_cost:,.2f} UZS")
    print(f"Electricity (Tok): {elec_cost:,.2f} UZS")
    print(f"Incassation (Inkassatsiya): {incass_cost:,.2f} UZS")
    print(f"BTech Fee: {btech_cost:,.2f} UZS")
    print(f"Glob Fee: {glob_cost:,.2f} UZS")
    print(f"TOTAL REAL EXPENSE: {total_expense:,.2f} UZS")
    print(f"NET PROFIT: {net_profit:,.2f} UZS")
    print(f"MARGIN: {margin:.2f}%\n")
