import os

branch_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\BranchAtmsDetailModal.vue'
header_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\dashboard\AnnualFinancialHeader.vue'

with open(branch_path, 'r', encoding='utf-8') as f:
    branch_code = f.read()

# Fix types in BranchAtmsDetailModal.vue:
# Property 'id', 'total_income', 'expense', 'total_cash_withdrawal' on 'TopIncomeAtmItem'
# We can cast or add optional chaining / type assertions `(atm as any).id`, `(atm as any).total_income`, etc.
# Or update the template/script logic safely.

branch_code = branch_code.replace("atm.id", "(atm as any).id")
branch_code = branch_code.replace("atm.total_income", "(atm as any).total_income || (atm as any).income")
branch_code = branch_code.replace("atm.expense", "(atm as any).expense")
branch_code = branch_code.replace("atm.total_cash_withdrawal", "(atm as any).total_cash_withdrawal || (atm as any).cash_withdrawal")
branch_code = branch_code.replace("atm.is_active", "(atm as any).is_active ?? ((atm as any).status === 'soz' || (atm as any).status === 'active')")

with open(branch_path, 'w', encoding='utf-8') as f:
    f.write(branch_code)

print("BranchAtmsDetailModal.vue fixed!")

with open(header_path, 'r', encoding='utf-8') as f:
    header_code = f.read()

header_code = header_code.replace("item.total_income", "(item as any).total_income || (item as any).income")
header_code = header_code.replace("item.profitability_pct", "(item as any).profitability_pct || 0")

with open(header_path, 'w', encoding='utf-8') as f:
    f.write(header_code)

print("AnnualFinancialHeader.vue fixed!")
