import os

branch_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\BranchAtmsDetailModal.vue'
with open(branch_path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
for i, line in enumerate(lines, 1):
    print(f"{i}: {line}")
