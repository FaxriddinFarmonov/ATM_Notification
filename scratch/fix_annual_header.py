import os

header_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\dashboard\AnnualFinancialHeader.vue'

with open(header_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix undefined checks in AnnualFinancialHeader.vue
content = content.replace("formatUzSum(currentData.income || currentData.total_income)", "formatUzSum(currentData.income || currentData.total_income || 0)")
content = content.replace("formatUzSum(currentData.total_income)", "formatUzSum(currentData.total_income || 0)")
content = content.replace("currentData.profitability_pct", "(currentData.profitability_pct ?? 0)")

with open(header_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("AnnualFinancialHeader.vue template fixed!")
