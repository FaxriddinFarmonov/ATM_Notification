import os

file_path = r"C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\AiBankomatPortalHub.vue"

new_code = """<template>
  <div class="relative overflow-hidden rounded-3xl bg-slate-950 border border-slate-800 p-6 lg:p-10 shadow-2xl space-y-8 text-white select-none">
    <!-- Ambient Backdrop Lighting Glows -->
    <div class="absolute -top-36 left-1/2 -translate-x-1/2 w-[500px] h-[500px] bg-sky-500/15 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute -bottom-36 left-1/2 -translate-x-1/2 w-[500px] h-[500px] bg-purple-500/15 rounded-full blur-3xl pointer-events-none"></div>

    <!-- Top Header Badge & Title -->
    <div class="text-center space-y-2 relative z-10">
      <div class="inline-flex items-center gap-2 px-4 py-1 rounded-full bg-slate-900/90 border border-slate-800 text-sky-400 text-[11px] font-black uppercase tracking-widest shadow-inner">
        <span class="w-2 h-2 rounded-full bg-sky-400 animate-ping"></span>
        <span>TURON BANK SUN'IY INTELLEKT PORTALI</span>
      </div>
      <h2 class="text-3xl sm:text-5xl font-black tracking-tight text-white flex items-center justify-center gap-3 drop-shadow-md">
        <span>AI Bankomat</span>
      </h2>
      <p class="text-xs sm:text-sm text-slate-400 font-medium max-w-xl mx-auto">
        Bankomatlar tarmog'ining sun'iy intellekt portali, moliyaviy tahlil va bashoratlar markazi
      </p>
    </div>

    <!-- Main Grid: Left Column Cards (4) — Center Large TuronBank Emblem — Right Column Cards (4) -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center relative z-10">
      
      <!-- Left Column: 4 Functional Cards -->
      <div class="lg:col-span-4 space-y-3.5">
        <!-- 1. AI Bankomat -->
        <div
          @click="handleCardClick('ai-studio')"
          class="flex items-center justify-between p-4 rounded-2xl bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800 hover:border-sky-500/50 transition-all duration-200 group shadow-md cursor-pointer transform hover:-translate-y-0.5 active:scale-98"
        >
          <div class="flex items-center gap-3.5 min-w-0">
            <div class="p-3 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/20 group-hover:scale-110 group-hover:bg-sky-500/20 transition-all shrink-0">
              <Sparkles class="w-5 h-5" />
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="text-xs sm:text-sm font-bold text-white group-hover:text-sky-300 transition-colors truncate">AI Bankomat Portali</span>
                <span class="px-2 py-0.2 rounded-full text-[9px] font-black bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">LIVE</span>
              </div>
              <p class="text-[11px] text-slate-400 truncate mt-0.5">Bankomatlar faoliyati bo'yicha AI tavsiyalar</p>
            </div>
          </div>
          <Maximize2 class="w-4 h-4 text-slate-500 group-hover:text-sky-400 transition-colors shrink-0 ml-2" />
        </div>

        <!-- 2. Boshqaruv & Moliyaviy KPI -->
        <div
          @click="handleCardClick('overview')"
          class="flex items-center justify-between p-4 rounded-2xl bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800 hover:border-indigo-500/50 transition-all duration-200 group shadow-md cursor-pointer transform hover:-translate-y-0.5 active:scale-98"
        >
          <div class="flex items-center gap-3.5 min-w-0">
            <div class="p-3 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 group-hover:scale-110 group-hover:bg-indigo-500/20 transition-all shrink-0">
              <LayoutDashboard class="w-5 h-5" />
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="text-xs sm:text-sm font-bold text-white group-hover:text-indigo-300 transition-colors truncate">Boshqaruv & KPI Xulosasi</span>
                <span class="px-2 py-0.2 rounded-full text-[9px] font-black bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">KPI</span>
              </div>
              <p class="text-[11px] text-slate-400 truncate mt-0.5">Daromad, foyda va umumiy xarajatlar</p>
            </div>
          </div>
          <Maximize2 class="w-4 h-4 text-slate-500 group-hover:text-indigo-400 transition-colors shrink-0 ml-2" />
        </div>

        <!-- 3. Filiallar Reytingi -->
        <div
          @click="handleCardClick('regions')"
          class="flex items-center justify-between p-4 rounded-2xl bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800 hover:border-emerald-500/50 transition-all duration-200 group shadow-md cursor-pointer transform hover:-translate-y-0.5 active:scale-98"
        >
          <div class="flex items-center gap-3.5 min-w-0">
            <div class="p-3 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 group-hover:scale-110 group-hover:bg-emerald-500/20 transition-all shrink-0">
              <MapPin class="w-5 h-5" />
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="text-xs sm:text-sm font-bold text-white group-hover:text-emerald-300 transition-colors truncate">Filiallar Reytingi</span>
                <span class="px-2 py-0.2 rounded-full text-[9px] font-black bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">FILIAL</span>
              </div>
              <p class="text-[11px] text-slate-400 truncate mt-0.5">Hududlar bo'yicha daromad va aylanma</p>
            </div>
          </div>
          <Maximize2 class="w-4 h-4 text-slate-500 group-hover:text-emerald-400 transition-colors shrink-0 ml-2" />
        </div>

        <!-- 4. Top Daromad ATMlar -->
        <div
          @click="handleCardClick('top-income')"
          class="flex items-center justify-between p-4 rounded-2xl bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800 hover:border-emerald-500/50 transition-all duration-200 group shadow-md cursor-pointer transform hover:-translate-y-0.5 active:scale-98"
        >
          <div class="flex items-center gap-3.5 min-w-0">
            <div class="p-3 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 group-hover:scale-110 group-hover:bg-emerald-500/20 transition-all shrink-0">
              <TrendingUp class="w-5 h-5" />
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="text-xs sm:text-sm font-bold text-white group-hover:text-emerald-300 transition-colors truncate">Top Daromad ATMlar</span>
                <span class="px-2 py-0.2 rounded-full text-[9px] font-black bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">TOP</span>
              </div>
              <p class="text-[11px] text-slate-400 truncate mt-0.5">Eng rentabelli va ko'p daromad keltirgan</p>
            </div>
          </div>
          <Maximize2 class="w-4 h-4 text-slate-500 group-hover:text-emerald-400 transition-colors shrink-0 ml-2" />
        </div>
      </div>

      <!-- Center Orbital Core with PROMINENT LARGER TuronBank Logo Emblem -->
      <div class="lg:col-span-4 flex flex-col items-center justify-center my-6 lg:my-0 relative">
        <div class="relative w-80 h-80 sm:w-96 sm:h-96 flex items-center justify-center">
          <!-- Outer Pulsing Neon Rings -->
          <div class="absolute inset-0 rounded-full border border-sky-500/20 animate-ping opacity-30"></div>
          <div class="absolute inset-4 rounded-full border-2 border-indigo-500/30"></div>
          <div class="absolute inset-10 rounded-full border-2 border-dashed border-sky-400/40 animate-spin-slow"></div>
          <div class="absolute inset-16 rounded-full border border-purple-500/25"></div>

          <!-- Central Core Glow Container (Expanded Large Size) -->
          <div class="relative z-10 w-48 h-48 sm:w-56 sm:h-56 rounded-full bg-slate-900 border-4 border-sky-400/60 shadow-[0_0_80px_rgba(56,189,248,0.4)] flex flex-col items-center justify-center p-4 group hover:scale-105 transition-transform duration-300 cursor-pointer">
            <!-- Official TuronBank Emblem Logo (Increased Size to 120) -->
            <TuronBankIcon
              :size="120"
              primary-color="#1d4ed8"
              secondary-color="#38bdf8"
              wave-color="#ffffff"
              glow-color="#38bdf8"
              :show-glow="true"
              id="ai-center-logo-large"
            />
            <div class="mt-1 px-3 py-0.5 rounded-full bg-sky-500/20 border border-sky-400/40 text-[10px] font-black text-sky-300 tracking-wider uppercase shadow">
              TURON BANK
            </div>
          </div>

          <!-- 4 Database Nodes (ATM, MONITOR, FILIAL, SERVIS) -->
          <div class="absolute top-2 left-2 px-2.5 py-1 rounded-lg bg-slate-900/95 border border-slate-700 text-[10px] font-mono text-sky-400 flex items-center gap-1.5 shadow-lg">
            <Database class="w-3.5 h-3.5 text-sky-400 animate-pulse" /> DB • ATM
          </div>

          <div class="absolute top-2 right-2 px-2.5 py-1 rounded-lg bg-slate-900/95 border border-slate-700 text-[10px] font-mono text-indigo-400 flex items-center gap-1.5 shadow-lg">
            <Database class="w-3.5 h-3.5 text-indigo-400 animate-pulse" /> DB • MONITOR
          </div>

          <div class="absolute bottom-2 left-2 px-2.5 py-1 rounded-lg bg-slate-900/95 border border-slate-700 text-[10px] font-mono text-emerald-400 flex items-center gap-1.5 shadow-lg">
            <Database class="w-3.5 h-3.5 text-emerald-400 animate-pulse" /> DB • FILIAL
          </div>

          <div class="absolute bottom-2 right-2 px-2.5 py-1 rounded-lg bg-slate-900/95 border border-slate-700 text-[10px] font-mono text-purple-400 flex items-center gap-1.5 shadow-lg">
            <Database class="w-3.5 h-3.5 text-purple-400 animate-pulse" /> DB • SERVIS
          </div>
        </div>
      </div>

      <!-- Right Column: 4 Functional Cards -->
      <div class="lg:col-span-4 space-y-3.5">
        <!-- 5. Top Xarajat ATMlar -->
        <div
          @click="handleCardClick('top-expense')"
          class="flex items-center justify-between p-4 rounded-2xl bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800 hover:border-rose-500/50 transition-all duration-200 group shadow-md cursor-pointer transform hover:-translate-y-0.5 active:scale-98"
        >
          <div class="flex items-center gap-3.5 min-w-0">
            <div class="p-3 rounded-xl bg-rose-500/10 text-rose-400 border border-rose-500/20 group-hover:scale-110 group-hover:bg-rose-500/20 transition-all shrink-0">
              <TrendingDown class="w-5 h-5" />
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="text-xs sm:text-sm font-bold text-white group-hover:text-rose-300 transition-colors truncate">Top Xarajat ATMlar</span>
                <span class="px-2 py-0.2 rounded-full text-[9px] font-black bg-rose-500/20 text-rose-400 border border-rose-500/30">XARAJAT</span>
              </div>
              <p class="text-[11px] text-slate-400 truncate mt-0.5">Sarf-xarajatlari yuqori bankomatlar</p>
            </div>
          </div>
          <Maximize2 class="w-4 h-4 text-slate-500 group-hover:text-rose-400 transition-colors shrink-0 ml-2" />
        </div>

        <!-- 6. Muammoli & Relokatsiya -->
        <div
          @click="handleCardClick('loss-making')"
          class="flex items-center justify-between p-4 rounded-2xl bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800 hover:border-rose-500/50 transition-all duration-200 group shadow-md cursor-pointer transform hover:-translate-y-0.5 active:scale-98"
        >
          <div class="flex items-center gap-3.5 min-w-0">
            <div class="p-3 rounded-xl bg-rose-500/10 text-rose-400 border border-rose-500/20 group-hover:scale-110 group-hover:bg-rose-500/20 transition-all shrink-0">
              <AlertTriangle class="w-5 h-5" />
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="text-xs sm:text-sm font-bold text-white group-hover:text-rose-300 transition-colors truncate">Muammoli & Relokatsiya</span>
                <span class="px-2 py-0.2 rounded-full text-[9px] font-black bg-rose-500/20 text-rose-400 border border-rose-500/30">MUHIM</span>
              </div>
              <p class="text-[11px] text-slate-400 truncate mt-0.5">Zarardagi va ko'chirish tavsiya etilgan</p>
            </div>
          </div>
          <Maximize2 class="w-4 h-4 text-slate-500 group-hover:text-rose-400 transition-colors shrink-0 ml-2" />
        </div>

        <!-- 7. AI Prognoz & Trendlar -->
        <div
          @click="handleCardClick('ai-studio')"
          class="flex items-center justify-between p-4 rounded-2xl bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800 hover:border-purple-500/50 transition-all duration-200 group shadow-md cursor-pointer transform hover:-translate-y-0.5 active:scale-98"
        >
          <div class="flex items-center gap-3.5 min-w-0">
            <div class="p-3 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20 group-hover:scale-110 group-hover:bg-purple-500/20 transition-all shrink-0">
              <Bot class="w-5 h-5" />
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="text-xs sm:text-sm font-bold text-white group-hover:text-purple-300 transition-colors truncate">AI Prognoz & Trendlar</span>
                <span class="px-2 py-0.2 rounded-full text-[9px] font-black bg-purple-500/20 text-purple-300 border border-purple-500/30">LLM</span>
              </div>
              <p class="text-[11px] text-slate-400 truncate mt-0.5">Kelgusi davr uchun AI xulosalar</p>
            </div>
          </div>
          <Maximize2 class="w-4 h-4 text-slate-500 group-hover:text-purple-400 transition-colors shrink-0 ml-2" />
        </div>

        <!-- 8. ATM Texnik Holat & Servis -->
        <div
          @click="handleCardClick('ai-studio')"
          class="flex items-center justify-between p-4 rounded-2xl bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800 hover:border-sky-500/50 transition-all duration-200 group shadow-md cursor-pointer transform hover:-translate-y-0.5 active:scale-98"
        >
          <div class="flex items-center gap-3.5 min-w-0">
            <div class="p-3 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/20 group-hover:scale-110 group-hover:bg-sky-500/20 transition-all shrink-0">
              <Wrench class="w-5 h-5" />
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="text-xs sm:text-sm font-bold text-white group-hover:text-sky-300 transition-colors truncate">ATM Texnik Holat & Servis</span>
                <span class="px-2 py-0.2 rounded-full text-[9px] font-black bg-sky-500/20 text-sky-400 border border-sky-500/30">SERVIS</span>
              </div>
              <p class="text-[11px] text-slate-400 truncate mt-0.5">Nosozliklar va texnik xizmat tahlili</p>
            </div>
          </div>
          <Maximize2 class="w-4 h-4 text-slate-500 group-hover:text-sky-400 transition-colors shrink-0 ml-2" />
        </div>
      </div>

    </div>

    <!-- Bottom Action Pill Buttons -->
    <div class="flex flex-wrap items-center justify-center gap-3 relative z-10 pt-2">
      <button
        @click="handleCardClick('ai-studio')"
        class="px-6 py-2.5 rounded-full bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-extrabold text-xs shadow-lg shadow-indigo-500/25 border border-blue-400/30 transition-all cursor-pointer active:scale-95 flex items-center gap-2"
      >
        <Sparkles class="w-4 h-4" />
        <span>AI Xizmatlar Portali</span>
      </button>

      <button
        @click="handleCardClick('regions')"
        class="px-6 py-2.5 rounded-full bg-slate-900 hover:bg-slate-800 text-sky-300 font-extrabold text-xs border border-slate-800 hover:border-sky-500/40 transition-all cursor-pointer active:scale-95 flex items-center gap-2"
      >
        <Building2 class="w-4 h-4" />
        <span>Filiallar Tahlili</span>
      </button>

      <button
        @click="handleCardClick('overview')"
        class="px-6 py-2.5 rounded-full bg-slate-900 hover:bg-slate-800 text-indigo-300 font-extrabold text-xs border border-slate-800 hover:border-indigo-500/40 transition-all cursor-pointer active:scale-95 flex items-center gap-2"
      >
        <LayoutDashboard class="w-4 h-4" />
        <span>Boshqaruv KPI</span>
      </button>
    </div>

    <!-- FULL SCREEN EXECUTIVE MODAL FOR CLICKED SECTION ("Katta ekranda ochiladi") -->
    <Teleport to="body">
      <div
        v-if="isModalOpen"
        class="fixed inset-0 z-50 overflow-y-auto bg-slate-950/95 backdrop-blur-2xl flex flex-col p-4 sm:p-6 transition-all duration-300"
        tabindex="0"
        @keydown.escape="closeModal"
      >
        <!-- Modal Top Bar -->
        <div class="flex items-center justify-between p-4 sm:p-5 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-2xl mb-6 sticky top-0 z-30">
          <div class="flex items-center gap-3.5">
            <div class="p-2.5 rounded-xl bg-sky-500/15 text-sky-400 border border-sky-500/30">
              <component :is="activeModalMeta.icon" class="w-6 h-6" />
            </div>
            <div>
              <div class="flex items-center gap-2">
                <h3 class="text-lg sm:text-xl font-extrabold text-white">
                  {{ activeModalMeta.title }}
                </h3>
                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase bg-sky-500/20 text-sky-400 border border-sky-500/30">
                  KATTA EKRAN REJIMIDA
                </span>
              </div>
              <p class="text-xs text-slate-400 mt-0.5">
                {{ activeModalMeta.description }}
              </p>
            </div>
          </div>

          <div class="flex items-center gap-3">
            <button
              type="button"
              @click="closeModal"
              class="inline-flex items-center gap-2 px-4 py-2 text-xs font-bold text-slate-300 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-xl transition-all active:scale-95 cursor-pointer"
            >
              <X class="w-4 h-4 text-rose-400" />
              <span>Yopish (ESC)</span>
            </button>
          </div>
        </div>

        <!-- Filter Bar inside Modal -->
        <div class="mb-6">
          <AnalyticsFilterToolbar />
        </div>

        <!-- Modal Dynamic Main Content -->
        <div class="flex-1 rounded-2xl bg-slate-900/40 border border-slate-800/80 p-4 sm:p-6 shadow-inner overflow-x-hidden">
          <OverviewTab v-if="activeTabKey === 'overview'" />
          <RegionsRankingTab v-else-if="activeTabKey === 'regions'" />
          <TopIncomeTab v-else-if="activeTabKey === 'top-income'" />
          <TopExpenseTab v-else-if="activeTabKey === 'top-expense'" />
          <LossMakingTab v-else-if="activeTabKey === 'loss-making'" />
          <AiStudioTab v-else-if="activeTabKey === 'ai-studio'" />
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import TuronBankIcon from '@/components/common/TuronBankIcon.vue';
import AnalyticsFilterToolbar from '@/components/analytics/AnalyticsFilterToolbar.vue';
import OverviewTab from '@/components/analytics/OverviewTab.vue';
import RegionsRankingTab from '@/components/analytics/RegionsRankingTab.vue';
import TopIncomeTab from '@/components/analytics/TopIncomeTab.vue';
import TopExpenseTab from '@/components/analytics/TopExpenseTab.vue';
import LossMakingTab from '@/components/analytics/LossMakingTab.vue';
import AiStudioTab from '@/components/analytics/AiStudioTab.vue';

import {
  Sparkles,
  LayoutDashboard,
  MapPin,
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  Bot,
  Wrench,
  Database,
  Maximize2,
  Building2,
  X
} from 'lucide-vue-next';

import type { AnalyticsTabType } from '@/stores/analyticsStore';

const emit = defineEmits<{
  (e: 'selectTab', tab: AnalyticsTabType): void;
}>();

const isModalOpen = ref(false);
const activeTabKey = ref<AnalyticsTabType>('overview');

const activeModalMeta = computed(() => {
  switch (activeTabKey.value) {
    case 'overview':
      return {
        title: 'Boshqaruv va KPI Xulosasi',
        description: "Turon Bank bankomatlar tarmog'ining to'liq daromad, sof foyda va sarf-xarajatlar tahlili",
        icon: LayoutDashboard
      };
    case 'regions':
      return {
        title: 'Filiallar Reytingi va Hududiy Tahlil',
        description: "Barcha viloyat va filiallar bo'yicha ATMlar daromadi, rentabelligi va xarajatlar taqsimoti",
        icon: MapPin
      };
    case 'top-income':
      return {
        title: 'Top Daromad Keltiruvchi Bankomatlar',
        description: "Eng yuqori sof foyda va moliyaviy samaradorlik ko'rsatgan yetakchi ATMlar ro'yxati",
        icon: TrendingUp
      };
    case 'top-expense':
      return {
        title: 'Top Xarajatli Bankomatlar Tahlili',
        description: "Ta'mirlash, zapchast va operatsion sarf-xarajatlari eng yuqori bo'lgan ATMlar tahlili",
        icon: TrendingDown
      };
    case 'loss-making':
      return {
        title: 'Muammoli & Relokatsiya Tavsiyasi',
        description: "Zarar keltirayotgan bankomatlar va ularni samaraliroq manzilga ko'chirish AI tavsiyalari",
        icon: AlertTriangle
      };
    case 'ai-studio':
    default:
      return {
        title: 'AI Bankomat Sun'iy Intellekt Portali',
        description: "Ollama LLM va AI algoritmlari asosidagi bashoratlar hamda chuqur biznes tahlili",
        icon: Sparkles
      };
  }
});

function handleCardClick(tab: AnalyticsTabType) {
  activeTabKey.value = tab;
  isModalOpen.value = true;
  emit('selectTab', tab);
}

function closeModal() {
  isModalOpen.value = false;
}
</script>

<style scoped>
@keyframes spinSlow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.animate-spin-slow {
  animation: spinSlow 20s linear infinite;
}
</style>
"""

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_code)

print("Updated AiBankomatPortalHub.vue with large logo & fullscreen modal")
