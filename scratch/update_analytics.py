import os

file_path = r"C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\views\AiAnalyticsView.vue"

new_content = """<template>
  <div class="space-y-6">
    <!-- Top Hero Showcase: AI Bankomat Portal Hub -->
    <AiBankomatPortalHub @select-tab="store.setTab($event)" />

    <!-- Tab Navigation Bar -->
    <div class="flex items-center gap-1.5 p-1.5 bg-gray-100/80 dark:bg-slate-800/80 backdrop-blur-md rounded-2xl border border-gray-200/80 dark:border-slate-700/80 overflow-x-auto">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        type="button"
        class="relative flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-bold transition-all duration-200 whitespace-nowrap flex-shrink-0"
        :class="
          store.activeTab === tab.id
            ? 'bg-white dark:bg-slate-900 text-purple-700 dark:text-purple-300 shadow-sm border border-gray-200/60 dark:border-slate-700'
            : 'text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-200 hover:bg-white/50 dark:hover:bg-slate-900/40'
        "
        @click="store.setTab(tab.id)"
      >
        <component :is="tab.icon" class="w-4 h-4" />
        <span>{{ tab.label }}</span>
        <span
          v-if="tab.badge"
          class="px-1.5 py-0.2 text-[10px] rounded-full font-extrabold"
          :class="tab.badgeClass"
        >
          {{ tab.badge }}
        </span>
      </button>
    </div>

    <!-- Filter Toolbar -->
    <AnalyticsFilterToolbar />

    <!-- Tab Content -->
    <div class="transition-opacity duration-200">
      <OverviewTab v-if="store.activeTab === 'overview'" />
      <RegionsRankingTab v-else-if="store.activeTab === 'regions'" />
      <TopIncomeTab v-else-if="store.activeTab === 'top-income'" />
      <TopExpenseTab v-else-if="store.activeTab === 'top-expense'" />
      <LossMakingTab v-else-if="store.activeTab === 'loss-making'" />
      <AiStudioTab v-else-if="store.activeTab === 'ai-studio'" />
    </div>

    <!-- Modals -->
    <SingleAtmAiModal />
    <RegionAiModal />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import {
  LayoutDashboard,
  MapPin,
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  Bot
} from 'lucide-vue-next';
import { useAnalyticsStore, type AnalyticsTabType } from '@/stores/analyticsStore';
import AiBankomatPortalHub from '@/components/analytics/AiBankomatPortalHub.vue';
import AnalyticsFilterToolbar from '@/components/analytics/AnalyticsFilterToolbar.vue';
import OverviewTab from '@/components/analytics/OverviewTab.vue';
import RegionsRankingTab from '@/components/analytics/RegionsRankingTab.vue';
import TopIncomeTab from '@/components/analytics/TopIncomeTab.vue';
import TopExpenseTab from '@/components/analytics/TopExpenseTab.vue';
import LossMakingTab from '@/components/analytics/LossMakingTab.vue';
import AiStudioTab from '@/components/analytics/AiStudioTab.vue';
import SingleAtmAiModal from '@/components/analytics/SingleAtmAiModal.vue';
import RegionAiModal from '@/components/analytics/RegionAiModal.vue';

const store = useAnalyticsStore();

const tabs: Array<{
  id: AnalyticsTabType;
  label: string;
  icon: unknown;
  badge?: string;
  badgeClass?: string;
}> = [
  {
    id: 'overview',
    label: 'Boshqaruv KPI',
    icon: LayoutDashboard
  },
  {
    id: 'regions',
    label: 'Filiallar Reytingi',
    icon: MapPin
  },
  {
    id: 'top-income',
    label: 'Top Daromad',
    icon: TrendingUp,
    badge: 'TOP',
    badgeClass: 'bg-emerald-100 dark:bg-emerald-500/20 text-emerald-700 dark:text-emerald-400'
  },
  {
    id: 'top-expense',
    label: 'Top Xarajat',
    icon: TrendingDown
  },
  {
    id: 'loss-making',
    label: 'Muammoli & Relokatsiya',
    icon: AlertTriangle,
    badge: 'MUHIM',
    badgeClass: 'bg-rose-100 dark:bg-rose-500/20 text-rose-700 dark:text-rose-400'
  },
  {
    id: 'ai-studio',
    label: 'AI Tahlil Portali',
    icon: Bot,
    badge: 'LLM',
    badgeClass: 'bg-purple-100 dark:bg-purple-500/20 text-purple-700 dark:text-purple-300'
  }
];

onMounted(() => {
  store.fetchCurrentTabData();
});
</script>
"""

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated successfully")
