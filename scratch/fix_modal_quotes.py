import os

modal_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\BranchAtmsDetailModal.vue'
with open(modal_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix single quote in ko'rsatilmagan inside single quotes
fixed_content = content.replace(
    "{{ atm.address || 'Manzil ko'rsatilmagan' }}",
    "{{ atm.address || \"Manzil ko'rsatilmagan\" }}"
)

with open(modal_path, 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("Fixed BranchAtmsDetailModal.vue quotes successfully!")
