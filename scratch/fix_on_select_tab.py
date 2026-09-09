import os

tab_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\AiStudioTab.vue'
with open(tab_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'const store = useAnalyticsStore();',
    'const store = useAnalyticsStore();\nfunction onSelectTab(tabId: any) { store.setTab(tabId); }'
)

with open(tab_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("AiStudioTab.vue onSelectTab function added!")
