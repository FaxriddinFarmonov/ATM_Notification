import os

branch_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\BranchAtmsDetailModal.vue'
with open(branch_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(160, min(300, len(lines))):
    print(f"{i+1}: {lines[i]}", end="")
