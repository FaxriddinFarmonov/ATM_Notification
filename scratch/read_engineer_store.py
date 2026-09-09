import os

store_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\stores\engineerStore.ts'
with open(store_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(content[:2500])
