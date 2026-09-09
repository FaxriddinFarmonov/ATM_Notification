import os

# 1. Update src/api/endpoints.ts
endpoints_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\api\endpoints.ts'
with open(endpoints_path, 'r', encoding='utf-8') as f:
    endpoints_code = f.read()

if 'models:' not in endpoints_code:
    endpoints_code = endpoints_code.replace(
        "lossMaking: '/analytics/atms/loss-making/'",
        "lossMaking: '/analytics/atms/loss-making/',\n    models: '/analytics/models/'"
    )
    with open(endpoints_path, 'w', encoding='utf-8') as f:
        f.write(endpoints_code)
    print("Updated endpoints.ts")

# 2. Update src/services/analyticsService.ts
analytics_service_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\services\analyticsService.ts'
with open(analytics_service_path, 'r', encoding='utf-8') as f:
    service_code = f.read()

if 'getModelAnalytics' not in service_code:
    new_method = '''
  async getModelAnalytics(): Promise<any> {
    const { data } = await http.get('/analytics/models/');
    return data;
  },'''
    service_code = service_code.replace(
      "async getLossMaking(params: AnalyticsQueryParams = {}): Promise<LossMakingAtmItem[]> {",
      new_method + "\n\n  async getLossMaking(params: AnalyticsQueryParams = {}): Promise<LossMakingAtmItem[]> {"
    )
    with open(analytics_service_path, 'w', encoding='utf-8') as f:
        f.write(service_code)
    print("Updated analyticsService.ts")

# 3. Update ModellarStatistikaView.vue
modellar_view_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\views\ModellarStatistikaView.vue'

modellar_vue_code = '''<template>
  <div class="space-y-6 pb-12 animate-fade-in">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white dark:bg-slate-800/90 p-6 rounded-2xl border border-slate-200 dark:border-slate-700/60 shadow-sm">
      <div>
        <div class="flex items-center gap-3">
          <div class="p-3 bg-purple-500/10 text-purple-600 dark:text-purple-400 rounded-xl">
            <Cpu class="w-7 h-7" />
          </div>
          <div>
            <h1 class="text-xl font-bold text-slate-900 dark:text-white tracking-tight">
              Modellar Statistikasi va Telemetriyasi
            </h1>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              ATM va terminallar modellari bo'yicha real apparat telemetriyasi va pul aylanmalari
            </p>
          </div>
        </div>
      </div>

      <!-- Action: Refresh -->
      <div class="flex items-center gap-2">
        <button
          @click="loadData(true)"
          :disabled="loading"
          class="px-4 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-700 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-200 text-xs font-semibold transition-all flex items-center gap-2 shadow-sm"
        >
          <RefreshCw :class="{ 'animate-spin': loading }" class="w-4 h-4 text-purple-500" />
          <span>Yangilash</span>
        </button>
      </div>
    </div>

    <!-- Loading Skeleton -->
    <div v-if="loading && !apiData" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="i in 4" :key="i" class="h-28 bg-slate-100 dark:bg-slate-800/60 rounded-2xl animate-pulse"></div>
    </div>

    <template v-else-if="apiData">
      <!-- 4 Top KPI Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-white dark:bg-slate-800/90 p-5 rounded-2xl border border-slate-200 dark:border-slate-700/60 shadow-sm flex items-center gap-4">
          <div class="p-3.5 rounded-2xl bg-purple-500/10 text-purple-600 dark:text-purple-400">
            <Cpu class="w-6 h-6" />
          </div>
          <div>
            <span class="text-xs text-slate-500 dark:text-slate-400 font-medium">Barcha Modellari</span>
            <p class="text-xl font-bold text-slate-900 dark:text-white mt-0.5">{{ apiData.total_models_count }} xil model</p>
          </div>
        </div>

        <div class="bg-white dark:bg-slate-800/90 p-5 rounded-2xl border border-slate-200 dark:border-slate-700/60 shadow-sm flex items-center gap-4">
          <div class="p-3.5 rounded-2xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
            <Award class="w-6 h-6" />
          </div>
          <div>
            <span class="text-xs text-slate-500 dark:text-slate-400 font-medium">Eng Ommabop Model</span>
            <p class="text-base font-bold text-slate-900 dark:text-white mt-0.5 line-clamp-1">
              {{ apiData.top_popular_model?.model || '---' }}
            </p>
            <span class="text-[10px] text-emerald-600 dark:text-emerald-400 font-semibold">
              {{ apiData.top_popular_model?.total || 0 }} ta bankomat ({{ apiData.top_popular_model?.vendor }})
            </span>
          </div>
        </div>

        <div class="bg-white dark:bg-slate-800/90 p-5 rounded-2xl border border-slate-200 dark:border-slate-700/60 shadow-sm flex items-center gap-4">
          <div class="p-3.5 rounded-2xl bg-teal-500/10 text-teal-600 dark:text-teal-400">
            <Coins class="w-6 h-6" />
          </div>
          <div>
            <span class="text-xs text-slate-500 dark:text-slate-400 font-medium">Eng Yuqori Qoldiq</span>
            <p class="text-base font-bold text-slate-900 dark:text-white mt-0.5 line-clamp-1">
              {{ apiData.top_cash_model?.model || '---' }}
            </p>
            <span class="text-[10px] text-teal-600 dark:text-teal-400 font-semibold">
              {{ formatBillion(apiData.top_cash_model?.total_cash || 0) }}
            </span>
          </div>
        </div>

        <div class="bg-white dark:bg-slate-800/90 p-5 rounded-2xl border border-slate-200 dark:border-slate-700/60 shadow-sm flex items-center gap-4">
          <div class="p-3.5 rounded-2xl bg-sky-500/10 text-sky-600 dark:text-sky-400">
            <Activity class="w-6 h-6" />
          </div>
          <div>
            <span class="text-xs text-slate-500 dark:text-slate-400 font-medium">O'rtacha Samaradorlik</span>
            <p class="text-xl font-bold text-sky-600 dark:text-sky-400 mt-0.5">{{ apiData.overall_uptime }}%</p>
          </div>
        </div>
      </div>

      <!-- Charts Row -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Donut Chart: Modellar bo'yicha taqsimot -->
        <div class="bg-white dark:bg-slate-800/90 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-700/60 p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <PieChart class="w-4 h-4 text-purple-500" />
              <span>Modellar Bo'yicha Taqsimot (Soni)</span>
            </h3>
            <span class="text-xs text-slate-400 font-medium">Jami {{ apiData.total_atms_count }} ta ATM</span>
          </div>

          <div class="h-64">
            <DonutChart :data="modelChartData" />
          </div>

          <div class="flex flex-wrap justify-center gap-3 mt-6">
            <div
              v-for="item in modelStats"
              :key="item.model"
              class="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-50 dark:bg-slate-900/50 border border-slate-200/60 dark:border-slate-700/50 text-xs"
            >
              <span class="w-2.5 h-2.5 rounded-full" :style="{ backgroundColor: item.color }"></span>
              <span class="font-semibold text-slate-800 dark:text-slate-200">{{ item.model }}</span>
              <span class="font-bold text-purple-600 dark:text-purple-400">{{ item.count }} ta</span>
            </div>
          </div>
        </div>

        <!-- Progress Bars: Modellar samaradorligi (Uptime %) -->
        <div class="bg-white dark:bg-slate-800/90 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-700/60 p-6 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <BarChart3 class="w-4 h-4 text-emerald-500" />
                <span>Modellar Samaradorligi va Ishlash Ulushi</span>
              </h3>
              <span class="text-xs text-emerald-600 dark:text-emerald-400 font-semibold">Online / Total %</span>
            </div>

            <div class="space-y-4 my-2">
              <div v-for="item in apiData.models" :key="item.model" class="space-y-1.5">
                <div class="flex items-center justify-between text-xs font-semibold">
                  <span class="text-slate-800 dark:text-slate-200 flex items-center gap-2">
                    <span>{{ item.model }}</span>
                    <span class="text-[10px] px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-700/60 text-slate-500">
                      {{ item.vendor }}
                    </span>
                  </span>
                  <span :class="uptimeTextClass(item.uptime)">{{ item.uptime }}%</span>
                </div>
                <div class="w-full h-2.5 bg-slate-100 dark:bg-slate-700/60 rounded-full overflow-hidden">
                  <div
                    class="h-full rounded-full transition-all duration-500"
                    :style="{ width: `${item.uptime}%`, backgroundColor: getPerformanceColor(item.uptime) }"
                  ></div>
                </div>
              </div>
            </div>
          </div>

          <div class="mt-4 pt-4 border-t border-slate-100 dark:border-slate-700/60 text-[11px] text-slate-400 flex items-center justify-between">
            <span>BTech telemetriyasi orqali real InService statusi</span>
            <span class="font-bold text-emerald-500 flex items-center gap-1">
              <CheckCircle2 class="w-3.5 h-3.5" /> 100% Real Ma'lumot
            </span>
          </div>
        </div>
      </div>

      <!-- Detail Interactive Table -->
      <div class="bg-white dark:bg-slate-800/90 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-700/60 overflow-hidden">
        <div class="p-6 border-b border-slate-200 dark:border-slate-700/60 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div>
            <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <Layers class="w-5 h-5 text-purple-500" />
              <span>Modellar Bo'yicha Batafsil Real Tahlil</span>
            </h3>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              Har bir model uchun jami soni, online/offline, kasseta pul qoldig'i va o'rtacha ko'rsatkichlar
            </p>
          </div>

          <!-- Search filter for table -->
          <div class="relative w-full sm:w-64">
            <Search class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              v-model="tableSearch"
              type="text"
              placeholder="Model yoki vendor nomi..."
              class="w-full pl-9 pr-3 py-2 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-700 text-xs text-slate-800 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="bg-slate-50 dark:bg-slate-900/60 border-b border-slate-200 dark:border-slate-700/60 text-slate-500 dark:text-slate-400 uppercase font-semibold">
              <tr>
                <th class="px-6 py-3.5">Model Nomi</th>
                <th class="px-4 py-3.5">Ishlab Chiqaruvchi (Vendor)</th>
                <th class="px-4 py-3.5 text-center">Jami Soni</th>
                <th class="px-4 py-3.5 text-center">Online (Soz)</th>
                <th class="px-4 py-3.5 text-center">Offline (Nosoz)</th>
                <th class="px-4 py-3.5 text-right">Jami Pul Qoldig'i (UZS)</th>
                <th class="px-4 py-3.5 text-right">O'rtacha Qoldiq / ATM</th>
                <th class="px-4 py-3.5 text-center">Samaradorlik %</th>
                <th class="px-6 py-3.5 text-center">Holati</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-700/60">
              <tr v-if="filteredModels.length === 0">
                <td colspan="9" class="px-6 py-12 text-center text-slate-400">
                  <EmptyState message="Mos model ma'lumoti topilmadi" />
                </td>
              </tr>

              <tr
                v-for="item in filteredModels"
                :key="item.model"
                class="hover:bg-slate-50/80 dark:hover:bg-slate-700/40 transition-colors group"
              >
                <td class="px-6 py-4 font-bold text-slate-900 dark:text-white text-sm group-hover:text-purple-500 transition-colors">
                  {{ item.model }}
                </td>

                <td class="px-4 py-4 font-medium text-slate-600 dark:text-slate-300">
                  <span class="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-200 font-semibold text-[11px]">
                    {{ item.vendor }}
                  </span>
                </td>

                <td class="px-4 py-4 text-center font-bold text-slate-900 dark:text-white text-sm">
                  {{ item.total }} ta
                </td>

                <td class="px-4 py-4 text-center font-bold text-emerald-600 dark:text-emerald-400">
                  {{ item.online }}
                </td>

                <td class="px-4 py-4 text-center font-bold text-red-500 dark:text-red-400">
                  {{ item.offline }}
                </td>

                <td class="px-4 py-4 text-right font-bold text-emerald-600 dark:text-emerald-400 text-sm">
                  {{ formatAmount(item.total_cash) }}
                </td>

                <td class="px-4 py-4 text-right font-medium text-slate-700 dark:text-slate-300">
                  {{ formatAmount(item.avg_cash) }}
                </td>

                <td class="px-4 py-4 text-center font-bold" :class="uptimeTextClass(item.uptime)">
                  {{ item.uptime }}%
                </td>

                <td class="px-6 py-4 text-center">
                  <span
                    :class="uptimeBadgeClass(item.uptime)"
                    class="px-3 py-1 rounded-full text-xs font-bold border inline-flex items-center gap-1"
                  >
                    <span :class="uptimeDotClass(item.uptime)" class="w-1.5 h-1.5 rounded-full"></span>
                    {{ item.status_label }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import DonutChart from '@/components/charts/DonutChart.vue';
import EmptyState from '@/components/common/EmptyState.vue';
import { analyticsService } from '@/services/analyticsService';
import type { DoughnutChartData } from '@/types/api';
import {
  Cpu,
  Award,
  Coins,
  Activity,
  PieChart,
  BarChart3,
  Layers,
  Search,
  RefreshCw,
  CheckCircle2
} from 'lucide-vue-next';

const PALETTE = ['#7C4DFF', '#00BFA5', '#F59E0B', '#3B82F6', '#EC4899', '#10B981', '#EF4444', '#6366F1'];

const loading = ref(true);
const apiData = ref<any>(null);
const tableSearch = ref('');

async function loadData(force = false) {
  loading.value = true;
  try {
    const data = await analyticsService.getModelAnalytics();
    apiData.value = data;
  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  loadData();
});

const filteredModels = computed(() => {
  if (!apiData.value || !apiData.value.models) return [];
  if (!tableSearch.value.trim()) return apiData.value.models;
  const q = tableSearch.value.toLowerCase().trim();
  return apiData.value.models.filter((m: any) =>
    m.model.toLowerCase().includes(q) || m.vendor.toLowerCase().includes(q)
  );
});

const modelStats = computed(() => {
  if (!apiData.value || !apiData.value.models) return [];
  return apiData.value.models.map((item: any, idx: number) => ({
    model: item.model,
    count: item.total,
    color: PALETTE[idx % PALETTE.length]
  }));
});

const modelChartData = computed<DoughnutChartData>(() => ({
  labels: modelStats.value.map((m: any) => m.model),
  datasets: [
    {
      data: modelStats.value.map((m: any) => m.count),
      backgroundColor: modelStats.value.map((m: any) => m.color),
      borderWidth: 2
    }
  ]
}));

function formatAmount(num: number) {
  if (!num) return "0 so'm";
  return new Intl.NumberFormat('uz-UZ').format(num) + " so'm";
}

function formatBillion(num: number) {
  if (!num) return "0 so'm";
  const billions = num / 1_000_000_000;
  return `${billions.toFixed(2)} mlrd UZS`;
}

function getPerformanceColor(uptime: number): string {
  if (uptime >= 90) return '#10B981';
  if (uptime >= 70) return '#F59E0B';
  return '#EF4444';
}

function uptimeTextClass(uptime: number): string {
  if (uptime >= 90) return 'text-emerald-600 dark:text-emerald-400';
  if (uptime >= 70) return 'text-amber-600 dark:text-amber-400';
  return 'text-red-500 dark:text-red-400';
}

function uptimeBadgeClass(uptime: number): string {
  if (uptime >= 90) return 'bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800';
  if (uptime >= 70) return 'bg-amber-50 dark:bg-amber-950/60 text-amber-700 dark:text-amber-300 border-amber-200 dark:border-amber-800';
  return 'bg-red-50 dark:bg-red-950/60 text-red-700 dark:text-red-300 border-red-200 dark:border-red-800';
}

function uptimeDotClass(uptime: number): string {
  if (uptime >= 90) return 'bg-emerald-500';
  if (uptime >= 70) return 'bg-amber-500';
  return 'bg-red-500';
}
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.25s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
'''

with open(modellar_view_path, 'w', encoding='utf-8') as f:
    f.write(modellar_vue_code)

print("Updated ModellarStatistikaView.vue successfully!")
