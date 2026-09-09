path_view = r"C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\views\AiAnalyticsView.vue"

new_view = """<template>
  <div class="space-y-6">
    <!-- Top Hero Showcase: AI Bankomat Portal Hub (Main Feature Navigation) -->
    <AiBankomatPortalHub @select-tab="store.setTab($event)" />

    <!-- Global Filter Toolbar -->
    <AnalyticsFilterToolbar />

    <!-- Active Tab Content -->
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
import { useAnalyticsStore } from '@/stores/analyticsStore';
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

onMounted(() => {
  store.fetchCurrentTabData();
});
</script>
"""

with open(path_view, 'w', encoding='utf-8') as f:
    f.write(new_view)

print("Updated AiAnalyticsView.vue to remove redundant tab bar")
