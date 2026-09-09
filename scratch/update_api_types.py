import os

api_types_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\types\api.ts'

with open(api_types_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add missing fields to TopIncomeAtmItem, AtmListItem, AnnualFinancialItem if needed
if 'export interface TopIncomeAtmItem' in content:
    content = content.replace(
        'export interface TopIncomeAtmItem {',
        'export interface TopIncomeAtmItem {\n  id?: number;\n  total_income?: number;\n  expense?: number;\n  total_cash_withdrawal?: number;'
    )

if 'export interface AtmListItem' in content:
    content = content.replace(
        'export interface AtmListItem {',
        'export interface AtmListItem {\n  is_active?: boolean;'
    )

if 'export interface AnnualFinancialItem' in content:
    content = content.replace(
        'export interface AnnualFinancialItem {',
        'export interface AnnualFinancialItem {\n  total_income?: number;\n  profitability_pct?: number;'
    )

with open(api_types_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("api.ts updated successfully!")
