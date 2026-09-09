path_hub = r"C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\AiBankomatPortalHub.vue"
with open(path_hub, 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("  Building2,\n", "")

with open(path_hub, 'w', encoding='utf-8') as f:
    f.write(code)

print("Removed unused Building2 import from AiBankomatPortalHub.vue")
