import os

store_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\stores\engineerStore.ts'

with open(store_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix unescaped single quote in ro'yxatini
fixed_content = content.replace("ro'yxatini", "ro\\'yxatini")
fixed_content = fixed_content.replace("'Muhandislar ro'yxatini yuklashda xatolik yuz berdi'", "\"Muhandislar ro'yxatini yuklashda xatolik yuz berdi\"")

with open(store_path, 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("Fixed engineerStore.ts quote error successfully!")
