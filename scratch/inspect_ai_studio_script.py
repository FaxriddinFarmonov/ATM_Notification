import os

tab_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\AiStudioTab.vue'
with open(tab_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(230, min(280, len(lines))):
    print(f"{i+1}: {lines[i]}", end="")
