path = r"C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\AiBankomatPortalHub.vue"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("title: 'AI Bankomat Sun'iy Intellekt Portali',", "title: \"AI Bankomat Sun'iy Intellekt Portali\",")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed string literal apostrophe in AiBankomatPortalHub.vue")
