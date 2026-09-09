import os

store_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\stores\atmStore.ts'
with open(store_path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
for i in range(95, min(160, len(lines))):
    print(f"{i+1}: {lines[i]}")
