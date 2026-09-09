import os

# 1. Update DashboardAtmView.vue
dashboard_view_code = '''<template>
  <div class="space-y-6">
    <div v-if="dashboardStore.isLoading && !dashboardStore.data" class="space-y-6">
      <Skeleton height="10rem" />
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Skeleton v-for="i in 4" :key="i" height="14rem" />
      </div>
    </div>

    <ErrorState
      v-else-if="dashboardStore.error && !dashboardStore.data"
      :message="dashboardStore.error"
      :on-retry="() => dashboardStore.fetchDashboard()"/>

    <template v-else>
      <!-- Annual Financial Executive Header -->
      <AnnualFinancialHeader />

      <!-- Hududiy Filiallar Daromad Reytingi (Bar Chart) -->
      <BranchRevenueRanking />

      <!-- Yillar Bo'yicha Taqqoslash Portali -->
      <YearlyComparisonChart />

      <!-- 4 Executive Key Stat Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="JAMI ATM"
          :value="summary?.total_atms ?? '-'"
          :icon="Landmark"
          iconBg="bg-blue-500/10"
          iconColor="text-blue-500 dark:text-blue-400"
        />
        <StatCard
          title="SOZ"
          :value="summary?.soz ?? '-'"
          :icon="Wifi"
          iconBg="bg-emerald-500/10"
          iconColor="text-emerald-500 dark:text-emerald-400"
          :progress="dashboardStore.workingPercentage"
          progressLabel="Ishlab turibdi"
        />
        <StatCard
          title="NOSOZ"
          :value="summary?.nosoz ?? '-'"
          :icon="WifiOff"
          iconBg="bg-rose-500/10"
          iconColor="text-rose-500 dark:text-rose-400"
          :progress="dashboardStore.faultyPercentage"
          progressLabel="Nosoz ulushi"
        />
        <StatCard
          title="TA'MIRLASH SARFI"
          :value="formatSumShort(maintenance?.repair_cost)"
          :icon="Wrench"
          iconBg="bg-slate-800"
          iconColor="text-sky-400"
          :subtitle="`${maintenance?.repair_count ?? 0} ta protokol`"
        />
      </div>

      <!-- Charts & Region Status Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <DonutChartCard
          title="ALOQA DARAJASI"
          :data="{
            labels: ['Soz', 'Nosoz'],
            values: [summary?.soz ?? 0, summary?.nosoz ?? 0],
            colors: ['#10B981', '#F43F5E']
          }"
          :legend="[
            { label: 'Soz', value: summary?.soz ?? 0, color: '#10B981' },
            { label: 'Nosoz', value: summary?.nosoz ?? 0, color: '#F43F5E' }
          ]"
          legend-suffix=""
          :center-text="{ value: formatPercent(dashboardStore.workingPercentage), label: 'Soz ulushi' }"
        />

        <DonutChartCard
          title="KARTA TARQATISH"
          :data="cardMixData"
          :legend="cardMixLegend"
          :unavailable="!hasCardData"
          empty-message="Karta turi ma'lumoti mavjud emas"
          :center-text="{ value: (summary?.uzcard ?? 0) + (summary?.humo ?? 0), label: 'Jami ATM' }"/>

        <!-- Region Status List -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-800 p-5 lg:col-span-2 flex flex-col">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-sm font-bold text-slate-800 dark:text-slate-200">Viloyatlar Holati (Soz / Jami)</h3>
            <span class="text-xs text-slate-400 font-medium">Real-time status</span>
          </div>
          <div v-if="topRegions.length === 0" class="py-6">
            <EmptyState message="Viloyatlar bo'yicha ma'lumot mavjud emas" />
          </div>
          <div
            v-else
            class="space-y-3 overflow-y-auto pr-2 max-h-[240px] custom-scroll"
          >
            <div v-for="region in topRegions" :key="region.region" class="space-y-1.5">
              <div class="flex items-center justify-between text-xs font-semibold">
                <span class="text-slate-700 dark:text-slate-300 font-bold">{{ region.region }}</span>
                <span class="text-slate-500 dark:text-slate-400">
                  <span class="text-emerald-600 dark:text-emerald-400 font-extrabold">{{ region.soz }}</span>
                  <span class="mx-1 text-slate-300 dark:text-slate-600">/</span>
                  <span>{{ region.total }}</span>
                  <span class="ml-2 text-xs font-bold" :class="regionUptimeColor(region)">
                    ({{ formatPercent(regionUptime(region)) }})
                  </span>
                </span>
              </div>
              <div class="ai-progress-track ai-progress-track--sm">
                <div
                  class="ai-progress-fill"
                  :class="regionUptimeBar(region)"
                  :style="{ width: `${regionUptime(region)}%` }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Network Overview Bar Card -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-800 p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-sm font-bold text-slate-800 dark:text-slate-200">ATM Tarmog'i Umumiy Holati</h3>
          <span class="text-sm font-extrabold text-slate-900 dark:text-slate-100">Jami {{ summary?.total_atms ?? '-' }} ta ATM</span>
        </div>
        <div class="flex items-center gap-6 flex-wrap">
          <div>
            <p class="text-3xl font-black text-slate-900 dark:text-slate-100">{{ formatPercent(dashboardStore.workingPercentage) }}</p>
            <p class="text-xs font-medium text-slate-500 dark:text-slate-400">Tarmoq Samaradorligi</p>
          </div>
          <div class="flex-1 min-w-[200px]">
            <div class="h-2.5 ai-progress-track relative rounded-full overflow-hidden">
              <div
                class="split-fill split-fill--success"
                :style="{ width: `${dashboardStore.workingPercentage}%` }"
              ></div>
              <div
                class="split-fill split-fill--danger"
                :style="{
                  left: `${Math.max(0, dashboardStore.workingPercentage - 1.5)}%`,
                  width: `${dashboardStore.faultyPercentage + 1.5}%`
                }"
              ></div>
            </div>
            <div class="flex flex-wrap gap-5 mt-3 text-xs font-bold">
              <div class="flex items-center gap-2">
                <span class="w-2.5 h-2.5 bg-emerald-500 rounded-full"></span>
                <span class="text-slate-700 dark:text-slate-300">Soz {{ formatPercent(dashboardStore.workingPercentage) }}</span>
                <span class="text-slate-400 dark:text-slate-500">({{ summary?.soz ?? 0 }} ta)</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="w-2.5 h-2.5 bg-rose-500 rounded-full"></span>
                <span class="text-slate-700 dark:text-slate-300">Nosoz {{ formatPercent(dashboardStore.faultyPercentage) }}</span>
                <span class="text-slate-400 dark:text-slate-500">({{ summary?.nosoz ?? 0 }} ta)</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useDashboardStore } from '@/stores/dashboardStore';
import AnnualFinancialHeader from '@/components/dashboard/AnnualFinancialHeader.vue';
import BranchRevenueRanking from '@/components/dashboard/BranchRevenueRanking.vue';
import YearlyComparisonChart from '@/components/dashboard/YearlyComparisonChart.vue';
import StatCard from '@/components/dashboard/StatCard.vue';
import DonutChartCard from '@/components/dashboard/DonutChartCard.vue';
import Skeleton from '@/components/common/Skeleton.vue';
import ErrorState from '@/components/common/ErrorState.vue';
import EmptyState from '@/components/common/EmptyState.vue';
import { Landmark, Wifi, WifiOff, Wrench } from 'lucide-vue-next';
import { formatPercent, formatSumShort, safePercentage } from '@/utils/format';
import { onRefresh } from '@/composables/useRefreshBus';
import type { DashboardRegionStat } from '@/types/api';

const dashboardStore = useDashboardStore();

const summary = computed(() => dashboardStore.summary);
const maintenance = computed(() => dashboardStore.maintenance);
const topRegions = computed(() => dashboardStore.topRegions);

const hasCardData = computed(() => (summary.value?.uzcard ?? 0) + (summary.value?.humo ?? 0) > 0);
const cardMixData = computed(() => {
  const uzcard = summary.value?.uzcard ?? 0;
  const humo = summary.value?.humo ?? 0;
  return {
    labels: ['UZCARD', 'HUMO'],
    values: [uzcard, humo],
    colors: ['#3B82F6', '#06B6D4']
  };
});

const cardMixLegend = computed(() => {
  const total = (summary.value?.uzcard ?? 0) + (summary.value?.humo ?? 0);
  const asPct = (v: number) => (total ? Math.round((v / total) * 100) : 0);
  return [
    { label: 'UZCARD', value: asPct(summary.value?.uzcard ?? 0), color: '#3B82F6' },
    { label: 'HUMO', value: asPct(summary.value?.humo ?? 0), color: '#06B6D4' }
  ];
});

function regionUptime(r: DashboardRegionStat): number {
  return safePercentage(r.soz ?? 0, r.total);
}
function regionUptimeColor(r: DashboardRegionStat): string {
  const u = regionUptime(r);
  if (u >= 80) return 'text-emerald-600 dark:text-emerald-400';
  if (u >= 50) return 'text-amber-600 dark:text-amber-400';
  return 'text-rose-600 dark:text-rose-400';
}
function regionUptimeBar(r: DashboardRegionStat): string {
  const u = regionUptime(r);
  if (u >= 80) return 'ai-progress-fill--success';
  if (u >= 50) return 'ai-progress-fill--warning';
  return 'ai-progress-fill--danger';
}

onMounted(() => {
  dashboardStore.fetchDashboard();
});

onRefresh(() => dashboardStore.fetchDashboard());
</script>

<style scoped>
.hero-panel {
  position: relative;
  overflow: hidden;
  isolation: isolate;
}
.hero-panel__content {
  position: relative;
  z-index: 2;
}
.hero-panel__bg {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.hero-panel__grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(59, 130, 246, 0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59, 130, 246, 0.07) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: radial-gradient(ellipse at 50% 40%, black 0%, transparent 75%);
  -webkit-mask-image: radial-gradient(ellipse at 50% 40%, black 0%, transparent 75%);
  animation: hero-grid-pan 30s linear infinite;
}

.split-fill {
  position: absolute;
  top: 0;
  bottom: 0;
  border-radius: 9999px;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1), left 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.split-fill--success {
  left: 0;
  background: linear-gradient(90deg, #059669 0%, #10b981 50%, #34d399 100%);
  box-shadow: 0 0 14px rgba(16, 185, 129, 0.5);
  z-index: 1;
}

.split-fill--danger {
  background: linear-gradient(90deg, #e11d48 0%, #f43f5e 50%, #fb7185 100%);
  box-shadow: 0 0 14px rgba(244, 63, 94, 0.5);
  z-index: 2;
}

.custom-scroll {
  scrollbar-width: thin;
  scrollbar-color: rgba(59, 130, 246, 0.3) transparent;
}
.custom-scroll::-webkit-scrollbar {
  width: 5px !important;
}
.custom-scroll::-webkit-scrollbar-thumb {
  background: rgba(59, 130, 246, 0.3) !important;
  border-radius: 9999px !important;
}
</style>
'''

dashboard_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\views\DashboardAtmView.vue'
with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(dashboard_view_code)

print("DashboardAtmView updated successfully!")
