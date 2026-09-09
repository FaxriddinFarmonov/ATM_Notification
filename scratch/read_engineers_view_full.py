import os

view_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\views\EngineersView.vue'
with open(view_path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
print(f"Total lines: {len(lines)}")
for i, line in enumerate(lines[100:], start=101):
    print(f"{i}: {line}")
