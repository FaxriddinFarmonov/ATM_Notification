import os

# 1. Update src/types/api.ts
api_types_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\types\api.ts'
with open(api_types_path, 'r', encoding='utf-8') as f:
    api_content = f.read()

# Add flexible optional properties to interfaces
if 'id?: number;' not in api_content:
    api_content = api_content.replace(
        'export interface TopIncomeAtmItem {',
        'export interface TopIncomeAtmItem {\n  id?: number;\n  total_income?: number;\n  expense?: number;\n  total_cash_withdrawal?: number;'
    )

if 'is_active?: boolean;' not in api_content:
    api_content = api_content.replace(
        'export interface AtmListItem {',
        'export interface AtmListItem {\n  is_active?: boolean;'
    )

if 'profitability_pct?: number;' not in api_content:
    api_content = api_content.replace(
        'export interface AnnualFinancialItem {',
        'export interface AnnualFinancialItem {\n  total_income?: number;\n  profitability_pct?: number;'
    )

with open(api_types_path, 'w', encoding='utf-8') as f:
    f.write(api_content)
print("api.ts updated!")

# 2. Fix BranchAtmsDetailModal.vue
branch_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\BranchAtmsDetailModal.vue'
with open(branch_path, 'r', encoding='utf-8') as f:
    branch_code = f.read()

branch_code = branch_code.replace("(atm as any).", "atm.")
branch_code = branch_code.replace("(atm as any)", "atm")
with open(branch_path, 'w', encoding='utf-8') as f:
    f.write(branch_code)
print("BranchAtmsDetailModal.vue cleaned up!")

# 3. Fix AnnualFinancialHeader.vue
header_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\dashboard\AnnualFinancialHeader.vue'
with open(header_path, 'r', encoding='utf-8') as f:
    header_code = f.read()

header_code = header_code.replace("(item as any).", "item.")
header_code = header_code.replace("(item as any)", "item")
with open(header_path, 'w', encoding='utf-8') as f:
    f.write(header_code)
print("AnnualFinancialHeader.vue cleaned up!")
