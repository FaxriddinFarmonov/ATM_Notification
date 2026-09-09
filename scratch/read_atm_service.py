import os

path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\services\atmService.ts'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

print(content[:2500])
