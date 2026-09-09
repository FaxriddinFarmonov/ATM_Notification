import os

# 1. Update FilialAylanmasiView.vue
filial_view_code = '''<template>
  <div class="space-y-6">
    <!-- Header Section -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2 mb-1">
          <span class="text-xs font-bold uppercase tracking-wider text-blue-600 dark:text-sky-400 flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            Turonbank ATB — Situatsion Markaz
          </span>
          <span class="text-xs text-gray-300 dark:text-slate-600">•</span>
          <span class="text-xs text-gray-500 dark:text-slate-400">20 ta Hududiy Filial</span>
        </div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-gray-900 dark:text-slate-100 tracking-tight">
          Filiallar Aylanmasi va <span class="bg-gradient-to-r from-blue-600 via-sky-500 to-teal-400 bg-clip-text text-transparent">Moliyaviy Tahlili</span>
        </h1>
        <p class="text-xs sm:text-sm text-gray-500 dark:text-slate-400 mt-1">
          Respublika bo'yicha barcha filiallar kesimida naqd pul chiqimi (aylanma), tushgan daromadlar, xarajatlar va rentabellik ko'rsatkichlari
        </p>
      </div>

      <!-- View Switcher (Jadval / Diagramma) -->
      <div class="flex items-center gap-1.5 bg-gray-100 dark:bg-slate-800/90 rounded-2xl border border-gray-200/80 dark:border-slate-700/80 p-1.5 self-start sm:self-auto shadow-sm">
        <button
          type="button"
          class="flex items-center gap-2 px-4 py-2 text-xs font-bold rounded-xl transition-all"
          :class="chartView === 'table'
            ? 'bg-white dark:bg-slate-900 text-blue-600 dark:text-sky-300 shadow-sm'
            : 'text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-200'"
          @click="chartView = 'table'"
        >
          <TableIcon class="w-4 h-4" />
          <span>Jadval</span>
        </button>
        <button
          type="button"
          class="flex items-center gap-2 px-4 py-2 text-xs font-bold rounded-xl transition-all"
          :class="chartView === 'chart'
            ? 'bg-white dark:bg-slate-900 text-blue-600 dark:text-sky-300 shadow-sm'
            : 'text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-200'"
          @click="chartView = 'chart'"
        >
          <BarChart3 class="w-4 h-4" />
          <span>Diagramma</span>
        </button>
      </div>
    </div>

    <!-- Top 4 Highlights Cards (20 ta filial) -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- 1. Tahlil qilingan filiallar -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-4 border border-gray-200/80 dark:border-slate-800 shadow-sm flex items-center gap-3.5">
        <div class="w-11 h-11 rounded-xl bg-blue-50 dark:bg-blue-500/15 flex items-center justify-center text-blue-600 dark:text-sky-300 flex-shrink-0">
          <Building2 class="w-5 h-5" />
        </div>
        <div>
          <p class="text-xs font-medium text-gray-500 dark:text-slate-400">Tahlil qilingan filiallar</p>
          <p class="text-xl font-black text-gray-900 dark:text-slate-100 mt-0.5">
            {{ store.regions.length || 20 }} ta filial
          </p>
        </div>
      </div>

      <!-- 2. 1-o'rindagi filial -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-4 border border-gray-200/80 dark:border-slate-800 shadow-sm flex items-center gap-3.5">
        <div class="w-11 h-11 rounded-xl bg-amber-50 dark:bg-amber-500/15 flex items-center justify-center text-amber-600 dark:text-amber-400 flex-shrink-0">
          <Award class="w-5 h-5" />
        </div>
        <div class="min-w-0">
          <p class="text-xs font-medium text-gray-500 dark:text-slate-400">1-o'rindagi filial</p>
          <p class="text-base font-black text-amber-600 dark:text-amber-400 truncate mt-0.5" :title="topLeaderBranch?.region">
            {{ topLeaderBranch?.region || '---' }}
          </p>
        </div>
      </div>

      <!-- 3. Eng yuqori marja -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-4 border border-gray-200/80 dark:border-slate-800 shadow-sm flex items-center gap-3.5">
        <div class="w-11 h-11 rounded-xl bg-emerald-50 dark:bg-emerald-500/15 flex items-center justify-center text-emerald-600 dark:text-emerald-400 flex-shrink-0">
          <TrendingUp class="w-5 h-5" />
        </div>
        <div>
          <p class="text-xs font-medium text-gray-500 dark:text-slate-400">Eng yuqori marja</p>
          <p class="text-xl font-black text-emerald-600 dark:text-emerald-400 mt-0.5">
            {{ highestMarginRegion?.profit_margin || 0 }}%
          </p>
        </div>
      </div>

      <!-- 4. Jami bankomatlar -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-4 border border-gray-200/80 dark:border-slate-800 shadow-sm flex items-center gap-3.5">
        <div class="w-11 h-11 rounded-xl bg-indigo-50 dark:bg-indigo-500/15 flex items-center justify-center text-indigo-600 dark:text-indigo-300 flex-shrink-0">
          <Landmark class="w-5 h-5" />
        </div>
        <div>
          <p class="text-xs font-medium text-gray-500 dark:text-slate-400">Jami bankomatlar</p>
          <p class="text-xl font-black text-gray-900 dark:text-slate-100 mt-0.5">
            {{ totalAtmsInRegions }} ta
          </p>
        </div>
      </div>
    </div>

    <!-- Filter Toolbar -->
    <div class="bg-white dark:bg-slate-900 rounded-2xl p-4 border border-gray-200/80 dark:border-slate-800 shadow-sm">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div class="flex flex-wrap items-center gap-2.5 flex-1 min-w-[280px]">
          <!-- Year Selector -->
          <div class="flex items-center gap-1.5 bg-gray-50 dark:bg-slate-800/80 border border-gray-200 dark:border-slate-700/80 rounded-xl px-3 py-1.5 text-xs text-gray-700 dark:text-slate-200">
            <Calendar class="w-3.5 h-3.5 text-blue-600 dark:text-sky-400" />
            <span class="font-medium text-gray-500 dark:text-slate-400">Yil:</span>
            <select
              v-model.number="store.selectedYear"
              class="bg-transparent font-bold text-gray-800 dark:text-slate-100 focus:outline-none cursor-pointer"
              @change="triggerRefresh"
            >
              <option :value="2026">2026</option>
              <option :value="2025">2025</option>
              <option :value="2024">2024</option>
            </select>
          </div>

          <!-- Month Selector -->
          <div class="flex items-center gap-1.5 bg-gray-50 dark:bg-slate-800/80 border border-gray-200 dark:border-slate-700/80 rounded-xl px-3 py-1.5 text-xs text-gray-700 dark:text-slate-200">
            <Clock class="w-3.5 h-3.5 text-purple-600 dark:text-purple-400" />
            <span class="font-medium text-gray-500 dark:text-slate-400">Oy:</span>
            <select
              v-model="store.selectedMonth"
              class="bg-transparent font-bold text-gray-800 dark:text-slate-100 focus:outline-none cursor-pointer"
              @change="triggerRefresh"
            >
              <option :value="undefined">Barchasi (Butun yil)</option>
              <option v-for="m in months" :key="m.value" :value="m.value">
                {{ m.label }}
              </option>
            </select>
          </div>

          <!-- Sort Selector -->
          <div class="flex items-center gap-1.5 bg-gray-50 dark:bg-slate-800/80 border border-gray-200 dark:border-slate-700/80 rounded-xl px-3 py-1.5 text-xs text-gray-700 dark:text-slate-200">
            <ArrowUpDown class="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            <span class="font-medium text-gray-500 dark:text-slate-400">Saralash:</span>
            <select
              v-model="store.selectedSortBy"
              class="bg-transparent font-bold text-gray-800 dark:text-slate-100 focus:outline-none cursor-pointer"
              @change="triggerRefresh"
            >
              <option value="profit">Sof foyda</option>
              <option value="income">Daromad</option>
              <option value="cash_withdrawal">Naqd chiqimi (Aylanma)</option>
              <option value="profit_margin">Rentabellik %</option>
              <option value="atms_count">Bankomatlar soni</option>
              <option value="expense">Xarajatlar</option>
            </select>
          </div>

          <!-- Limit Selector -->
          <div class="flex items-center gap-1.5 bg-gray-50 dark:bg-slate-800/80 border border-gray-200 dark:border-slate-700/80 rounded-xl px-3 py-1.5 text-xs text-gray-700 dark:text-slate-200">
            <SlidersHorizontal class="w-3.5 h-3.5 text-slate-500" />
            <span class="font-medium text-gray-500 dark:text-slate-400">Limit:</span>
            <select
              v-model.number="store.selectedLimit"
              class="bg-transparent font-bold text-gray-800 dark:text-slate-100 focus:outline-none cursor-pointer"
              @change="triggerRefresh"
            >
              <option :value="10">10 ta</option>
              <option :value="20">20 ta (Barcha filiallar)</option>
              <option :value="50">50 ta</option>
            </select>
          </div>
        </div>

        <!-- Refresh Button -->
        <button
          type="button"
          class="inline-flex items-center gap-1.5 px-3.5 py-1.5 text-xs font-bold text-blue-700 dark:text-sky-300 bg-blue-50 dark:bg-blue-500/15 hover:bg-blue-100 dark:hover:bg-blue-500/25 border border-blue-200/80 dark:border-blue-500/30 rounded-xl transition-all shadow-sm active:scale-95 disabled:opacity-50"
          :disabled="store.isRegionsLoading"
          @click="triggerRefresh"
        >
          <RefreshCw class="w-3.5 h-3.5" :class="{ 'animate-spin': store.isRegionsLoading }" />
          <span>Yangilash</span>
        </button>
      </div>
    </div>

    <!-- MAIN VIEW CONTENT: TABLE OR CHART -->
    <div v-if="chartView === 'table'" class="bg-white dark:bg-slate-900 rounded-2xl border border-gray-200/80 dark:border-slate-800 shadow-sm overflow-hidden">
      <!-- Search & Count Header inside Table -->
      <div class="p-4 border-b border-gray-100 dark:border-slate-800 flex flex-wrap items-center justify-between gap-3">
        <div class="flex items-center gap-2">
          <h3 class="text-sm font-extrabold text-gray-900 dark:text-slate-100">
            Filiallar Moliyaviy Reytingi va Aylanmasi
          </h3>
          <span class="text-xs px-2.5 py-0.5 rounded-full bg-blue-50 dark:bg-blue-500/20 text-blue-700 dark:text-sky-300 font-bold">
            {{ filteredRegions.length }} ta filial
          </span>
          <span class="text-xs text-slate-400 font-medium ml-2">(Filialni bosib bankomatlarini ko'ring)</span>
        </div>

        <div class="relative">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-gray-400 dark:text-slate-500" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Filial nomi bo'yicha qidirish..."
            class="w-64 pl-8 pr-3 py-1.5 text-xs bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-xl text-gray-800 dark:text-slate-100 placeholder-gray-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="store.isRegionsLoading && store.regions.length === 0" class="p-5 space-y-3">
        <Skeleton v-for="i in 8" :key="i" height="3rem" />
      </div>

      <!-- Error State -->
      <ErrorState
        v-else-if="store.regionsError && store.regions.length === 0"
        :message="store.regionsError"
        :on-retry="() => store.fetchRegions()"
      />

      <!-- Table -->
      <div v-else class="overflow-x-auto">
        <table class="w-full text-xs text-left">
          <thead class="bg-gray-50/90 dark:bg-slate-800/80 border-b border-gray-200 dark:border-slate-800 uppercase tracking-wider text-gray-500 dark:text-slate-400 font-bold">
            <tr>
              <th class="px-4 py-3.5 text-center w-12">#</th>
              <th class="px-4 py-3.5">Filial Nomi</th>
              <th class="px-4 py-3.5 text-center">Bankomatlar</th>
              <th class="px-4 py-3.5 text-right">Daromad</th>
              <th class="px-4 py-3.5 text-right">Naqd Chiqimi</th>
              <th class="px-4 py-3.5 text-right">Xarajatlar</th>
              <th class="px-4 py-3.5 text-right">Sof Foyda</th>
              <th class="px-4 py-3.5 text-center min-w-[140px]">Rentabellik %</th>
              <th class="px-4 py-3.5 text-right">O'rtacha Daromad / ATM</th>
              <th class="px-4 py-3.5">Eng Yaxshi ATM</th>
              <th class="px-4 py-3.5 text-center">AI Tahlil</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-slate-800 font-medium">
            <tr v-if="filteredRegions.length === 0">
              <td colspan="11" class="px-4 py-12">
                <EmptyState message="Hech qanday filial ma'lumoti topilmadi" />
              </td>
            </tr>
            <tr
              v-for="(r, idx) in filteredRegions"
              :key="r.region"
              @click="openBranchModal(r.region)"
              class="hover:bg-blue-50/50 dark:hover:bg-slate-800/80 cursor-pointer transition-colors group"
            >
              <!-- 1. Rank & Medal -->
              <td class="px-4 py-3 text-center">
                <span
                  v-if="idx === 0"
                  class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-amber-100 dark:bg-amber-500/20 text-amber-700 dark:text-amber-400 font-bold text-xs"
                >
                  🥇
                </span>
                <span
                  v-else-if="idx === 1"
                  class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 font-bold text-xs"
                >
                  🥈
                </span>
                <span
                  v-else-if="idx === 2"
                  class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-orange-100 dark:bg-orange-500/20 text-orange-700 dark:text-orange-400 font-bold text-xs"
                >
                  🥉
                </span>
                <span v-else class="text-gray-400 dark:text-slate-500 font-bold">
                  {{ idx + 1 }}
                </span>
              </td>

              <!-- 2. Filial Name -->
              <td class="px-4 py-3 font-extrabold text-gray-900 dark:text-slate-100 whitespace-nowrap text-sm group-hover:text-blue-600 dark:group-hover:text-sky-400 transition-colors">
                {{ r.region }}
              </td>

              <!-- 3. Bankomatlar (Total + soz/nosoz) -->
              <td class="px-4 py-3 text-center whitespace-nowrap">
                <div class="flex items-center justify-center gap-1.5">
                  <span class="font-extrabold text-gray-900 dark:text-slate-100">{{ r.total_atms }}</span>
                  <span class="text-[10px] text-gray-400 dark:text-slate-500">(</span>
                  <span class="text-[10px] text-emerald-600 dark:text-emerald-400 font-bold" :title="`Soz: ${r.soz_atms}`">{{ r.soz_atms }} soz</span>
                  <span class="text-[10px] text-gray-400 dark:text-slate-500">/</span>
                  <span class="text-[10px] text-rose-600 dark:text-rose-400 font-bold" :title="`Nosoz: ${r.nosoz_atms}`">{{ r.nosoz_atms }} nosoz</span>
                  <span class="text-[10px] text-gray-400 dark:text-slate-500">)</span>
                </div>
              </td>

              <!-- 4. Daromad -->
              <td class="px-4 py-3 text-right font-extrabold text-emerald-600 dark:text-emerald-400 whitespace-nowrap">
                {{ formatSumShort(r.total_income) }}
              </td>

              <!-- 5. Naqd Chiqimi (Aylanma) -->
              <td class="px-4 py-3 text-right text-gray-800 dark:text-slate-200 font-bold whitespace-nowrap">
                {{ formatSumShort(r.total_cash_withdrawal) }}
              </td>

              <!-- 6. Xarajatlar -->
              <td class="px-4 py-3 text-right whitespace-nowrap">
                <p class="font-extrabold text-rose-600 dark:text-rose-400">{{ formatSumShort(r.total_real_expense) }}</p>
                <p class="text-[10px] text-gray-400 dark:text-slate-500" :title="`Ta'mirlash zapchast: ${formatCurrency(r.maintenance_cost)}`">
                  Zapchast: {{ formatSumShort(r.maintenance_cost) }}
                </p>
              </td>

              <!-- 7. Sof Foyda -->
              <td class="px-4 py-3 text-right whitespace-nowrap">
                <span
                  class="font-black text-sm"
                  :class="r.net_profit >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'"
                >
                  {{ formatSumShort(r.net_profit) }}
                </span>
              </td>

              <!-- 8. Rentabellik % -->
              <td class="px-4 py-3 text-center whitespace-nowrap">
                <div class="flex items-center gap-2">
                  <div class="flex-1 h-2 bg-gray-100 dark:bg-slate-800 rounded-full overflow-hidden">
                    <div
                      class="h-full rounded-full transition-all duration-300"
                      :class="marginColorClass(r.profit_margin)"
                      :style="{ width: Math.min(100, Math.max(0, r.profit_margin)) + '%' }"
                    />
                  </div>
                  <span
                    class="font-extrabold text-xs min-w-[45px] text-right"
                    :class="marginTextColorClass(r.profit_margin)"
                  >
                    {{ r.profit_margin }}%
                  </span>
                </div>
              </td>

              <!-- 9. O'rtacha Daromad / ATM -->
              <td class="px-4 py-3 text-right text-gray-700 dark:text-slate-300 font-semibold whitespace-nowrap">
                {{ formatSumShort(r.avg_income_per_atm) }}
              </td>

              <!-- 10. Eng Yaxshi ATM -->
              <td class="px-4 py-3 whitespace-nowrap">
                <div v-if="r.top_atm" class="flex flex-col">
                  <span class="font-bold text-gray-900 dark:text-slate-100 truncate max-w-[130px]" :title="r.top_atm.name">
                    {{ r.top_atm.name }}
                  </span>
                  <span class="text-[10px] font-mono text-sky-600 dark:text-sky-400">
                    TID: {{ r.top_atm.terminal_id }} ({{ formatSumShort(r.top_atm.income) }})
                  </span>
                </div>
                <span v-else class="text-gray-400 dark:text-slate-500">---</span>
              </td>

              <!-- 11. AI Tahlil Tugmasi -->
              <td class="px-4 py-3 text-center whitespace-nowrap" @click.stop>
                <button
                  type="button"
                  class="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-bold text-blue-700 dark:text-sky-300 bg-blue-50 dark:bg-blue-500/15 hover:bg-blue-100 dark:hover:bg-blue-500/25 border border-blue-200 dark:border-blue-500/30 rounded-xl transition-all shadow-sm active:scale-95"
                  @click="store.openRegionAiModal(r.region)"
                >
                  <Bot class="w-3.5 h-3.5" />
                  <span>AI</span>
                </button>
              </td>
            </tr>
          </tbody>

          <!-- Table Summary Footer -->
          <tfoot class="bg-gray-50/90 dark:bg-slate-800/90 border-t border-gray-200 dark:border-slate-700 font-black">
            <tr>
              <td colspan="2" class="px-4 py-3.5 text-right text-xs uppercase tracking-wider text-gray-500 dark:text-slate-400">
                Jami / O'rtacha:
              </td>
              <td class="px-4 py-3.5 text-center text-gray-900 dark:text-slate-100">
                {{ totalAtmsInRegions }} ta
              </td>
              <td class="px-4 py-3.5 text-right text-emerald-600 dark:text-emerald-400">
                {{ formatSumShort(totals.income) }}
              </td>
              <td class="px-4 py-3.5 text-right text-gray-900 dark:text-slate-100">
                {{ formatSumShort(totals.cashWithdrawal) }}
              </td>
              <td class="px-4 py-3.5 text-right text-rose-600 dark:text-rose-400">
                {{ formatSumShort(totals.expense) }}
              </td>
              <td class="px-4 py-3.5 text-right text-emerald-600 dark:text-emerald-400">
                {{ formatSumShort(totals.profit) }}
              </td>
              <td class="px-4 py-3.5 text-center text-emerald-600 dark:text-emerald-400">
                {{ averageMargin }}%
              </td>
              <td class="px-4 py-3.5 text-right text-gray-700 dark:text-slate-300">
                {{ formatSumShort(averageIncomePerAtm) }}
              </td>
              <td colspan="2" class="px-4 py-3.5" />
            </tr>
          </tfoot>
        </table>
      </div>
    </div>

    <!-- DIAGRAMMA VIEW (Clean Executive Bar Chart - Line overlay removed) -->
    <div v-else class="bg-white dark:bg-slate-900 rounded-2xl border border-gray-200/80 dark:border-slate-800 p-6 shadow-sm">
      <div v-if="filteredRegions.length === 0" class="p-8">
        <EmptyState message="Diagramma uchun ma'lumot mavjud emas" />
      </div>
      <template v-else>
        <div class="flex items-center justify-between gap-4 mb-6 flex-wrap">
          <div>
            <h3 class="text-base font-extrabold text-gray-900 dark:text-slate-100">
              Filiallar Bo'yicha Moliyaviy Tushum Diagrammasi
            </h3>
            <p class="text-xs text-gray-500 dark:text-slate-400 mt-0.5">
              Filiallar bo'yicha tushgan jami daromadlar solishtirmasi
            </p>
          </div>
          <div class="flex items-center gap-4 text-xs font-bold">
            <span class="inline-flex items-center gap-1.5 text-sky-600 dark:text-sky-400">
              <span class="w-3.5 h-3.5 rounded-md bg-sky-500" />
              Daromad (mln UZS)
            </span>
          </div>
        </div>

        <div class="h-96">
          <DualAxisChart :data="chartData" y-axis-unit="mln UZS" />
        </div>
      </template>
    </div>

    <!-- Region AI Modal -->
    <RegionAiModal />

    <!-- Branch ATMs Detail Modal -->
    <BranchAtmsDetailModal />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useAnalyticsStore } from '@/stores/analyticsStore';
import { useBranchModal } from '@/composables/useBranchModal';
import {
  Building2,
  Award,
  TrendingUp,
  Landmark,
  Search,
  Bot,
  Calendar,
  Clock,
  ArrowUpDown,
  SlidersHorizontal,
  RefreshCw,
  Table as TableIcon,
  BarChart3
} from 'lucide-vue-next';
import { formatSumShort, formatCurrency } from '@/utils/format';
import Skeleton from '@/components/common/Skeleton.vue';
import ErrorState from '@/components/common/ErrorState.vue';
import EmptyState from '@/components/common/EmptyState.vue';
import DualAxisChart from '@/components/charts/DualAxisChart.vue';
import RegionAiModal from '@/components/analytics/RegionAiModal.vue';
import BranchAtmsDetailModal from '@/components/analytics/BranchAtmsDetailModal.vue';
import { onRefresh } from '@/composables/useRefreshBus';
import type { BarLineChartData } from '@/types/api';

const store = useAnalyticsStore();
const { openBranchModal } = useBranchModal();

const chartView = ref<'table' | 'chart'>('table');
const searchQuery = ref('');

const months = [
  { value: 1, label: 'Yanvar' },
  { value: 2, label: 'Fevral' },
  { value: 3, label: 'Mart' },
  { value: 4, label: 'Aprel' },
  { value: 5, label: 'May' },
  { value: 6, label: 'Iyun' },
  { value: 7, label: 'Iyul' },
  { value: 8, label: 'Avgust' },
  { value: 9, label: 'Sentabr' },
  { value: 10, label: 'Oktabr' },
  { value: 11, label: 'Noyabr' },
  { value: 12, label: 'Dekabr' }
];

const filteredRegions = computed(() => {
  if (!searchQuery.value.trim()) return store.regions;
  const q = searchQuery.value.toLowerCase().trim();
  return store.regions.filter((r) => r.region.toLowerCase().includes(q));
});

const topLeaderBranch = computed(() => {
  if (!store.regions || store.regions.length === 0) return null;
  return store.regions[0];
});

const highestMarginRegion = computed(() => {
  if (!store.regions || store.regions.length === 0) return null;
  return [...store.regions].sort((a, b) => b.profit_margin - a.profit_margin)[0];
});

const totalAtmsInRegions = computed(() => {
  return store.regions.reduce((sum, r) => sum + (r.total_atms || 0), 0);
});

const totals = computed(() => {
  const acc = {
    income: 0,
    cashWithdrawal: 0,
    expense: 0,
    profit: 0
  };
  for (const r of filteredRegions.value) {
    acc.income += r.total_income || 0;
    acc.cashWithdrawal += r.total_cash_withdrawal || 0;
    acc.expense += r.total_real_expense || 0;
    acc.profit += r.net_profit || 0;
  }
  return acc;
});

const averageMargin = computed(() => {
  if (filteredRegions.value.length === 0) return 0;
  const sum = filteredRegions.value.reduce((acc, r) => acc + (r.profit_margin || 0), 0);
  return (sum / filteredRegions.value.length).toFixed(1);
});

const averageIncomePerAtm = computed(() => {
  if (totalAtmsInRegions.value === 0) return 0;
  return Math.round(totals.value.income / totalAtmsInRegions.value);
});

function marginColorClass(margin: number): string {
  if (margin >= 80) return 'bg-emerald-500';
  if (margin >= 60) return 'bg-indigo-500';
  if (margin >= 40) return 'bg-amber-500';
  return 'bg-rose-500';
}

function marginTextColorClass(margin: number): string {
  if (margin >= 80) return 'text-emerald-600 dark:text-emerald-400';
  if (margin >= 60) return 'text-indigo-600 dark:text-indigo-400';
  if (margin >= 40) return 'text-amber-600 dark:text-amber-400';
  return 'text-rose-600 dark:text-rose-400';
}

// Clean bar chart without purple line graph overlay
const chartData = computed<BarLineChartData>(() => ({
  labels: filteredRegions.value.map((r) => r.region),
  datasets: [
    {
      type: 'bar',
      label: 'Daromad (mln UZS)',
      data: filteredRegions.value.map((r) => Math.round((r.total_income || 0) / 1000000)),
      backgroundColor: 'rgba(56, 189, 248, 0.85)',
      borderColor: '#38bdf8',
      borderWidth: 1,
      yAxisID: 'y'
    }
  ]
}));

async function triggerRefresh(): Promise<void> {
  await store.fetchRegions();
}

onMounted(() => {
  store.selectedLimit = 20;
  store.fetchRegions();
});

onRefresh(() => {
  store.fetchRegions();
});
</script>
'''

filial_view_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\views\FilialAylanmasiView.vue'
with open(filial_view_path, 'w', encoding='utf-8') as f:
    f.write(filial_view_code)

print("Updated FilialAylanmasiView.vue successfully!")
