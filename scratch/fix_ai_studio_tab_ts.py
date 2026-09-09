import os

tab_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\AiStudioTab.vue'
with open(tab_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove unused ArrowRight import
content = content.replace("ArrowRight,", "")
content = content.replace(", ArrowRight", "")

# Ensure onSelectTab function is exposed properly in script setup
if 'function onSelectTab' not in content:
    content = content.replace(
        "const studioRegion = ref('Toshkent sh.');",
        "const analyticsStore = useAnalyticsStore();\nfunction onSelectTab(tabId: any) { analyticsStore.setTab(tabId); }\nconst studioRegion = ref('Toshkent sh.');"
    )

with open(tab_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("AiStudioTab.vue clean fix applied!")
