import os

assign_modal_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\engineers\AssignAtmModal.vue'
detail_modal_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\engineers\EngineerDetailModal.vue'

for path in [assign_modal_path, detail_modal_path]:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace single quote in ko'rsatilmagan with escaped or double quoted
    content = content.replace("ko'rsatilmagan", "ko\\'rsatilmagan")
    content = content.replace("'Manzil ko\\'rsatilmagan'", '"Manzil ko\'rsatilmagan"')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixed Vue templates quote issue!")
