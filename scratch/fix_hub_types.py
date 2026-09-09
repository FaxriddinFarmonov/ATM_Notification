path = r"C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\AiBankomatPortalHub.vue"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("defineEmits<{\n  (e: 'selectTab', tab: string): void;\n}>();", "import type { AnalyticsTabType } from '@/stores/analyticsStore';\n\ndefineEmits<{\n  (e: 'selectTab', tab: AnalyticsTabType): void;\n}>();")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated AiBankomatPortalHub.vue")
