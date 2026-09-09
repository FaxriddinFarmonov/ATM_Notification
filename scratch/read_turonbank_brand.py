import os

icon_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\common\TuronBankIcon.vue'
brand_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\common\TuronBankBrand.vue'

with open(icon_path, 'r', encoding='utf-8') as f:
    print("=== TuronBankIcon.vue ===")
    print(f.read())

with open(brand_path, 'r', encoding='utf-8') as f:
    print("\n=== TuronBankBrand.vue ===")
    print(f.read())
