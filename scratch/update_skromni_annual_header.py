import os

annual_header_code = '''<template>
  <div class="w-full">
    <!-- Loading Skeleton -->
    <div v-if="isLoading" class="p-6 bg-slate-900 rounded-3xl border border-slate-800 animate-pulse space-y-4">
      <div class="h-6 w-48 bg-slate-800 rounded-lg"></div>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div v-for="i in 4" :key="i" class="h-24 bg-slate-800 rounded-2xl"></div>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="p-4 bg-rose-950/60 border border-rose-500/40 text-rose-200 rounded-2xl text-xs flex justify-between items-center">
      <span>{{ error }}</span>
      <button @click="loadData" class="px-3 py-1.5 bg-rose-800 hover:bg-rose-700 text-white rounded-xl font-bold transition-colors">
        Qayta urinish
      </button>
    </div>

    <!-- Main Content Panel -->
    <div v-else-if="currentData" class="p-6 sm:p-7 bg-slate-900/90 rounded-3xl border border-slate-800 shadow-xl text-white space-y-6">
      
      <!-- Top Title & Year Switcher Toolbar -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div class="flex items-center gap-3.5">
          <div class="p-3 rounded-2xl bg-blue-500/10 border border-blue-500/20 text-blue-400">
            <Building2 class="w-6 h-6" />
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-sky-400 uppercase tracking-widest">TURONBANK ATB</span>
              <span class="w-1.5 h-1.5 rounded-full bg-slate-600"></span>
              <span class="text-xs font-bold text-slate-400">Boshqaruv Hisoboti</span>
            </div>
            <h2 class="text-xl sm:text-2xl font-black text-white tracking-tight mt-0.5">
              Yillik Moliyaviy va Operatsion Ko'rsatkichlar
            </h2>
          </div>
        </div>

        <!-- Year Pills Selector -->
        <div class="flex items-center gap-1.5 p-1.5 rounded-2xl bg-slate-955 border border-slate-800 text-xs">
          <button
            v-for="y in yearsList"
            :key="y.year"
            @click="selectedYear = y.year"
            :class="[
              'px-3.5 py-1.5 rounded-xl font-bold transition-all flex items-center gap-1.5',
              selectedYear === y.year
                ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
            ]"
          >
            <Calendar class="w-3.5 h-3.5" />
            <span>{{ y.label }}</span>
          </button>
        </div>
      </div>

      <!-- 4 Top Executive KPI Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <!-- 1. Jami Daromad -->
        <div class="p-5 rounded-2xl bg-slate-950/80 border border-blue-500/20 shadow-sm relative overflow-hidden group">
          <div class="flex items-center justify-between text-xs font-bold text-slate-400 mb-1">
            <span>Jami Daromad:</span>
            <span class="p-1.5 rounded-lg bg-blue-500/10 text-sky-400">
              <Coins class="w-4 h-4" />
            </span>
          </div>
          <div class="text-xl sm:text-2xl font-black text-sky-400 mt-1">
            {{ formatUzSum(currentData.total_income) }}
          </div>
          <div class="text-[11px] text-slate-400 font-semibold mt-2 flex items-center gap-1">
            <span class="text-emerald-400 font-bold">ATMlar Tushumi</span>
            <span>({{ selectedYear }}-yil)</span>
          </div>
        </div>

        <!-- 2. Haqiqiy Rasxod -->
        <div class="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 shadow-sm relative overflow-hidden group">
          <div class="flex items-center justify-between text-xs font-bold text-slate-400 mb-1">
            <span>Haqiqiy Rasxodlar:</span>
            <span class="p-1.5 rounded-lg bg-slate-800 text-slate-300">
              <Receipt class="w-4 h-4" />
            </span>
          </div>
          <div class="text-xl sm:text-2xl font-black text-slate-200 mt-1">
            {{ formatUzSum(currentData.total_expense) }}
          </div>
          <div class="text-[11px] text-slate-400 font-semibold mt-2 truncate">
            Asosiy rasxod: <strong class="text-slate-300 font-bold">{{ getTopExpenseName(currentData.expenses_breakdown) }}</strong>
          </div>
        </div>

        <!-- 3. Sof Foyda (Net Profit) -->
        <div class="p-5 rounded-2xl bg-slate-950/80 border border-emerald-500/20 shadow-sm relative overflow-hidden group">
          <div class="flex items-center justify-between text-xs font-bold text-slate-400 mb-1">
            <span>Sof Foyda:</span>
            <span class="p-1.5 rounded-lg bg-emerald-500/10 text-emerald-400">
              <TrendingUp v-if="currentData.net_profit >= 0" class="w-4 h-4" />
              <TrendingDown v-else class="w-4 h-4" />
            </span>
          </div>
          <div :class="['text-xl sm:text-2xl font-black mt-1', currentData.net_profit >= 0 ? 'text-emerald-400' : 'text-rose-400']">
            {{ formatUzSum(currentData.net_profit) }}
          </div>
          <div class="text-[11px] text-slate-400 font-semibold mt-2 flex items-center gap-1">
            <span>Rentabellik:</span>
            <strong :class="currentData.profitability_pct >= 0 ? 'text-emerald-400' : 'text-rose-400'">
              {{ currentData.profitability_pct >= 0 ? '+' : '' }}{{ currentData.profitability_pct }}%
            </strong>
          </div>
        </div>

        <!-- 4. Naqd Pul Aylanmasi -->
        <div class="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 shadow-sm relative overflow-hidden group">
          <div class="flex items-center justify-between text-xs font-bold text-slate-400 mb-1">
            <span>Naqd Pul Yechish:</span>
            <span class="p-1.5 rounded-lg bg-indigo-500/10 text-indigo-400">
              <PieChart class="w-4 h-4" />
            </span>
          </div>
          <div class="text-xl sm:text-2xl font-black text-indigo-300 mt-1">
            {{ formatUzSum(currentData.cash_withdrawal) }}
          </div>
          <div class="text-[11px] text-slate-400 font-semibold mt-2">
            Aholi tomonidan yechilgan naqd
          </div>
        </div>
      </div>

      <!-- Expenses Breakdown Harmonious Executive Panel -->
      <div v-if="currentData.expenses_breakdown" class="p-5 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-3">
        <div class="flex items-center justify-between">
          <h3 class="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-blue-500"></span>
            Haqiqiy Rasxodlar Struktura Tahlili
          </h3>
          <span class="text-xs text-slate-400 font-medium">Jami: {{ formatUzSum(currentData.total_expense) }}</span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
          
          <!-- 1. Incassation -->
          <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition-colors">
            <div class="flex items-center justify-between text-[11px] text-slate-400 mb-1.5">
              <span class="font-bold text-slate-300 flex items-center gap-1.5">
                <Truck class="w-3.5 h-3.5 text-sky-400" /> Inkassatsiya
              </span>
              <span class="text-sky-400 font-extrabold">{{ getExpensePct(currentData.expenses_breakdown.incassation, currentData.total_expense) }}%</span>
            </div>
            <div class="text-xs font-extrabold text-white">
              {{ formatUzSum(currentData.expenses_breakdown.incassation) }}
            </div>
            <div class="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
              <div class="bg-sky-500 h-full rounded-full" :style="{ width: getExpensePct(currentData.expenses_breakdown.incassation, currentData.total_expense) + '%' }"></div>
            </div>
          </div>

          <!-- 2. Maintenance -->
          <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition-colors">
            <div class="flex items-center justify-between text-[11px] text-slate-400 mb-1.5">
              <span class="font-bold text-slate-300 flex items-center gap-1.5">
                <Wrench class="w-3.5 h-3.5 text-blue-400" /> Ta'mirlash
              </span>
              <span class="text-blue-400 font-extrabold">{{ getExpensePct(currentData.expenses_breakdown.maintenance, currentData.total_expense) }}%</span>
            </div>
            <div class="text-xs font-extrabold text-white">
              {{ formatUzSum(currentData.expenses_breakdown.maintenance) }}
            </div>
            <div class="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
              <div class="bg-blue-500 h-full rounded-full" :style="{ width: getExpensePct(currentData.expenses_breakdown.maintenance, currentData.total_expense) + '%' }"></div>
            </div>
          </div>

          <!-- 3. BTech & Glob -->
          <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition-colors">
            <div class="flex items-center justify-between text-[11px] text-slate-400 mb-1.5">
              <span class="font-bold text-slate-300 flex items-center gap-1.5">
                <FileText class="w-3.5 h-3.5 text-indigo-400" /> BTech & Glob
              </span>
              <span class="text-indigo-400 font-extrabold">{{ getExpensePct(currentData.expenses_breakdown.btech_glob, currentData.total_expense) }}%</span>
            </div>
            <div class="text-xs font-extrabold text-white">
              {{ formatUzSum(currentData.expenses_breakdown.btech_glob) }}
            </div>
            <div class="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
              <div class="bg-indigo-500 h-full rounded-full" :style="{ width: getExpensePct(currentData.expenses_breakdown.btech_glob, currentData.total_expense) + '%' }"></div>
            </div>
          </div>

          <!-- 4. Electricity -->
          <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition-colors">
            <div class="flex items-center justify-between text-[11px] text-slate-400 mb-1.5">
              <span class="font-bold text-slate-300 flex items-center gap-1.5">
                <Zap class="w-3.5 h-3.5 text-teal-400" /> Elektr Energiya
              </span>
              <span class="text-teal-400 font-extrabold">{{ getExpensePct(currentData.expenses_breakdown.electricity, currentData.total_expense) }}%</span>
            </div>
            <div class="text-xs font-extrabold text-white">
              {{ formatUzSum(currentData.expenses_breakdown.electricity) }}
            </div>
            <div class="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
              <div class="bg-teal-500 h-full rounded-full" :style="{ width: getExpensePct(currentData.expenses_breakdown.electricity, currentData.total_expense) + '%' }"></div>
            </div>
          </div>

          <!-- 5. Rent -->
          <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition-colors">
            <div class="flex items-center justify-between text-[11px] text-slate-400 mb-1.5">
              <span class="font-bold text-slate-300 flex items-center gap-1.5">
                <Home class="w-3.5 h-3.5 text-slate-400" /> Ijara To'lovi
              </span>
              <span class="text-slate-300 font-extrabold">{{ getExpensePct(currentData.expenses_breakdown.rent, currentData.total_expense) }}%</span>
            </div>
            <div class="text-xs font-extrabold text-white">
              {{ formatUzSum(currentData.expenses_breakdown.rent) }}
            </div>
            <div class="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
              <div class="bg-slate-600 h-full rounded-full" :style="{ width: getExpensePct(currentData.expenses_breakdown.rent, currentData.total_expense) + '%' }"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { analyticsService, type AnnualFinancialItem } from '@/services/analyticsService';
import {
  Building2,
  Calendar,
  TrendingUp,
  TrendingDown,
  Coins,
  PieChart,
  Receipt,
  Truck,
  Wrench,
  FileText,
  Zap,
  Home
} from 'lucide-vue-next';

const isLoading = ref(true);
const error = ref<string | null>(null);
const financialsMap = ref<Record<number, AnnualFinancialItem>>({});
const selectedYear = ref<number>(2026);

const yearsList = [
  { year: 2026, label: "2026-yil (6 oy)" },
  { year: 2025, label: "2025-yil" },
  { year: 2024, label: "2024-yil" },
];

const currentData = computed(() => financialsMap.value[selectedYear.value] || null);

async function loadData() {
  isLoading.value = true;
  error.value = null;
  try {
    const res = await analyticsService.getAnnualFinancials();
    const itemsList: AnnualFinancialItem[] = Array.isArray(res) 
      ? res 
      : (res?.years || (res as any)?.annual_financials || []);
      
    const map: Record<number, AnnualFinancialItem> = {};
    itemsList.forEach((item: AnnualFinancialItem) => {
      if (item && item.year) {
        map[item.year] = item;
      }
    });
    financialsMap.value = map;
  } catch (err: any) {
    console.error("Annual financials fetch error:", err);
    error.value = err?.message || "Yillik moliyaviy ma'lumotlarni yuklashda xatolik yuz berdi";
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  loadData();
});

function formatUzSum(val: number): string {
  if (val === undefined || val === null || isNaN(val)) return "0 so'm";
  const abs = Math.abs(val);
  if (abs >= 1_000_000_000_000) {
    return (val / 1_000_000_000_000).toFixed(2) + " Trln so'm";
  }
  if (abs >= 1_000_000_000) {
    return (val / 1_000_000_000).toFixed(2) + " Mlrd so'm";
  }
  if (abs >= 1_000_000) {
    return (val / 1_000_000).toFixed(2) + " Mln so'm";
  }
  if (abs >= 1_000) {
    return (val / 1_000).toFixed(1) + " MING so'm";
  }
  return val.toLocaleString('uz-UZ') + " so'm";
}

function getExpensePct(itemVal: number, totalVal: number): string {
  if (!totalVal || totalVal === 0 || !itemVal) return '0.0';
  return ((itemVal / totalVal) * 100).toFixed(1);
}

function getTopExpenseName(breakdown: AnnualFinancialItem['expenses_breakdown']): string {
  if (!breakdown) return "Mavjud emas";
  const items = [
    { name: "BTech & Glob", val: breakdown.btech_glob || 0 },
    { name: "Ta'mirlash", val: breakdown.maintenance || 0 },
    { name: "Inkassatsiya", val: breakdown.incassation || 0 },
    { name: "Elektr energiyasi", val: breakdown.electricity || 0 },
    { name: "Ijara", val: breakdown.rent || 0 }
  ];
  items.sort((a, b) => b.val - a.val);
  return items[0].val > 0 ? items[0].name : "Mavjud emas";
}
</script>
'''

header_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\dashboard\AnnualFinancialHeader.vue'
with open(header_path, 'w', encoding='utf-8') as f:
    f.write(annual_header_code)

print("AnnualFinancialHeader.vue updated successfully!")
