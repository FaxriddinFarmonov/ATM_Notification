import os

api_types_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\types\api.ts'

with open(api_types_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if 'export interface TopIncomeAtmItem {' in line:
        new_lines.append("  id?: number;\n")
        new_lines.append("  total_income?: number;\n")
        new_lines.append("  expense?: number;\n")
        new_lines.append("  total_cash_withdrawal?: number;\n")
    elif 'export interface AtmListItem {' in line:
        new_lines.append("  is_active?: boolean;\n")
    elif 'export interface AnnualFinancialItem {' in line:
        new_lines.append("  total_income?: number;\n")
        new_lines.append("  profitability_pct?: number;\n")

with open(api_types_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("api.ts interfaces patched!")
