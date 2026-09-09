import os

tab_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\AiStudioTab.vue'
with open(tab_path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
print(f"Total lines: {len(lines)}")
for i in range(0, min(120, len(lines))):
    print(f"{i+1}: {lines[i]}")
