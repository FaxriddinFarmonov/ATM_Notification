import os

branch_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\BranchAtmsDetailModal.vue'

with open(branch_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace mixed || and ?? operators with clear parenthesized logic
old_badge_condition = "atm.status === 'soz' || atm.is_active ?? (atm.status === 'soz' || atm.status === 'active') !== false"
new_badge_condition = "(atm.status === 'soz' || (atm.is_active ?? true))"

content = content.replace(old_badge_condition, new_badge_condition)

with open(branch_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("BranchAtmsDetailModal template syntax fixed!")
