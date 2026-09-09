import os

tab_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\AiStudioTab.vue'
with open(tab_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Hero Banner with AiBankomatPortalHub component
old_banner = '''    <!-- Hero Banner -->
    <div class="p-6 rounded-3xl bg-gradient-to-r from-purple-900/30 via-indigo-900/20 to-slate-900/30 border border-purple-500/30 relative overflow-hidden">
      <div class="relative z-10 flex flex-wrap items-center justify-between gap-4">
        <div class="space-y-1">
          <span class="text-xs font-bold uppercase tracking-wider text-purple-600 dark:text-purple-400">
            Turon Bank AI Studio
          </span>
          <h2 class="text-2xl font-extrabold text-gray-900 dark:text-slate-100">
            Mahalliy Ollama Sun'iy Intellekti Tahlil Portali
          </h2>
          <p class="text-xs text-gray-500 dark:text-slate-400 max-w-xl">
            Bankomatlar tarmog'i, viloyatlar moliyaviy oqimlari va texnik holatlarini chuqur tahlil qilib, inson tushunadigan o'zbek tilida tayyor tahliliy xulosalar yaratadi.
          </p>
        </div>

        <div class="flex items-center gap-3">
          <router-link
            :to="{ name: 'AtmAiList' }"
            class="px-4 py-2 text-xs font-bold text-purple-700 dark:text-purple-200 bg-purple-100 dark:bg-purple-500/20 hover:bg-purple-200 dark:hover:bg-purple-500/30 rounded-xl transition-colors flex items-center gap-1.5"
          >
            <Sparkles class="w-4 h-4" />
            <span>Bankomatlar AI Katalogi</span>
            <ArrowRight class="w-3.5 h-3.5" />
          </router-link>
        </div>
      </div>
    </div>'''

new_banner = '''    <!-- TuronBank AI Bankomat Central Hub Showcase -->
    <AiBankomatPortalHub @selectTab="onSelectTab" />'''

content = content.replace(old_banner, new_banner)

# Import AiBankomatPortalHub & useAnalyticsStore
if 'AiBankomatPortalHub' not in content:
    content = content.replace(
        "import { ref, computed } from 'vue';",
        "import { ref, computed } from 'vue';\nimport AiBankomatPortalHub from '@/components/analytics/AiBankomatPortalHub.vue';\nimport { useAnalyticsStore } from '@/stores/analyticsStore';"
    )

if 'onSelectTab' not in content:
    content = content.replace(
        "const isGeneratingRegion = ref(false);",
        "const analyticsStore = useAnalyticsStore();\nfunction onSelectTab(tabId: any) { analyticsStore.setTab(tabId); }\nconst isGeneratingRegion = ref(false);"
    )

with open(tab_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("AiStudioTab.vue updated with AiBankomatPortalHub!")
