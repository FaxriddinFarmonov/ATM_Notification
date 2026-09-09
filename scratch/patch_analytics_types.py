import os

analytics_types_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\types\analytics.ts'

with open(analytics_types_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add fields to TopIncomeAtmItem
content = content.replace(
    'export interface TopIncomeAtmItem {',
    'export interface TopIncomeAtmItem {\n  id?: number;\n  total_income?: number;\n  expense?: number;\n  total_cash_withdrawal?: number;'
)

# Add fields to AnnualFinancialItem
content = content.replace(
    'export interface AnnualFinancialItem {',
    'export interface AnnualFinancialItem {\n  total_income?: number;\n  profitability_pct?: number;'
)

with open(analytics_types_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("analytics.ts interface patched!")
