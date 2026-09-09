p = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\BranchAtmsDetailModal.vue'
with open(p, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('class="bg-slate-900"', 'class="bg-slate-900 text-white font-bold py-1"')

with open(p, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated BranchAtmsDetailModal options successfully!")
