import os

view_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\views\EngineersView.vue'
with open(view_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Total characters in EngineersView.vue: {len(content)}")
print(content[:3000])
