import os

hub_component_code = '''<template>
  <div class="relative overflow-hidden rounded-3xl bg-slate-950 border border-slate-800 p-6 lg:p-10 shadow-2xl space-y-8 text-white select-none">
    <!-- Ambient Backdrop Lighting Glows -->
    <div class="absolute -top-32 left-1/2 -translate-x-1/2 w-96 h-96 bg-sky-500/10 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute -bottom-32 left-1/2 -translate-x-1/2 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl pointer-events-none"></div>

    <!-- Header Section -->
    <div class="text-center space-y-2 relative z-10">
      <div class="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-slate-900 border border-slate-800 text-sky-400 text-[11px] font-black uppercase tracking-widest">
        <span>TURON BANK</span>
      </div>
      <h2 class="text-3xl sm:text-4xl font-black tracking-tight text-white flex items-center justify-center gap-3">
        <span>AI Bankomat</span>
      </h2>
      <p class="text-xs sm:text-sm text-slate-400 font-medium max-w-lg mx-auto">
        Bankomat tizimining sun'iy intellekt portali va moliyaviy bashoratlar markazi
      </p>
    </div>

    <!-- Main Central Hub Showcase Grid (Left Cards - Center TuronBank Core - Right Cards) -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center relative z-10">
      
      <!-- Left Column: 4 AI Cards -->
      <div class="lg:col-span-4 space-y-3.5">
        <!-- 1. AI Bankomat (LIVE) -->
        <router-link
          :to="{ name: 'AtmAiList' }"
          class="flex items-center justify-between p-3.5 rounded-2xl bg-slate-900/90 hover:bg-slate-800 border border-slate-800 hover:border-sky-500/40 transition-all duration-200 group shadow-md"
        >
          <div class="flex items-center gap-3 min-w-0">
            <div class="p-2.5 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/20 group-hover:scale-105 transition-transform shrink-0">
              <Sparkles class="w-5 h-5" />
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-white group-hover:text-sky-400 transition-colors truncate">AI Bankomat</span>
                <span class="px-2 py-0.2 rounded-full text-[9px] font-black bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">LIVE</span>
              </div>
              <p class="text-[11px] text-slate-400 truncate mt-0.5">Bankomat faoliyati bo'yicha AI tahlil va tavsiyalar</p>
            </div>
          </div>
        </router-link>

        <!-- 2. AI Xavf Baholash (SOON) -->
        <div class="flex items-center justify-between p-3.5 rounded-2xl bg-slate-900/60 border border-slate-800/80 opacity-90 transition-all group">
          <div class="flex items-center gap-3 min-w-0">
            <div class="p-2.5 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20 shrink-0">
              <ShieldAlert class="w-5 h-5" />
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-slate-200 truncate">AI Xavf Baholash</span>
                <span class="px-2 py-0.2 rounded-full text-[9px] font-black bg-amber-500/10 text-amber-400 border border-amber-500/30">SOON</span>
              </div>
              <p class="text-[11px] text-slate-400 truncate mt-0.5">Xavf darajasini AI orqali baholash tizimi</p>
            </div>
          </div>
        </div>

        <!-- 3. AI Anomaliyalar (SOON) -->
        <div class="flex items-center justify-between p-3.5 rounded-2xl bg-slate-900/60 border border-slate-800/80 opacity-90 transition-all group">
          <div class="flex items-center gap-3 min-w-0">
            <div class="p-2.5 rounded-xl bg-rose-500/10 text-rose-400 border border-rose-500/20 shrink-0">
              <AlertOctagon class="w-5 h-5" />
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-slate-200 truncate">AI Anomaliyalar</span>
                <span class="px-2 py-0.2 rounded-full text-[9px] font-black bg-amber-500/10 text-amber-400 border border-amber-500/30">SOON</span>
              </div>
              <p class="text-[11px] text-slate-400 truncate mt-0.5">Anomaliyalarni real vaqtda aniqlash</p>
            </div>
          </div>
        </div>

        <!-- 4. AI Servis Xarajatlari (SOON) -->
        <div class="flex items-center justify-between p-3.5 rounded-2xl bg-slate-900/60 border border-slate-800/80 opacity-90 transition-all group">
          <div class="flex items-center gap-3 min-w-0">
            <div class="p-2.5 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 shrink-0">
              <Wallet class="w-5 h-5" />
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-slate-200 truncate">AI Servis Xarajatlari</span>
                <span class="px-2 py-0.2 rounded-full text-[9px] font-black bg-amber-500/10 text-amber-400 border border-amber-500/30">SOON</span>
              </div>
              <p class="text-[11px] text-slate-400 truncate mt-0.5">Servis xarajatlarini optimallashtirish tavsiyalari</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Center Orbital Core with Official TuronBank Logo Emblem -->
      <div class="lg:col-span-4 flex flex-col items-center justify-center my-6 lg:my-0 relative">
        <div class="relative w-64 h-64 flex items-center justify-center">
          <!-- Outer Pulsing Neon Rings -->
          <div class="absolute inset-0 rounded-full border border-sky-500/20 animate-ping opacity-20"></div>
          <div class="absolute inset-3 rounded-full border border-indigo-500/30"></div>
          <div class="absolute inset-8 rounded-full border border-dashed border-sky-400/30 animate-spin-slow"></div>

          <!-- Central Core Glow Container -->
          <div class="relative z-10 w-36 h-36 rounded-full bg-slate-900 border-2 border-sky-500/40 shadow-[0_0_50px_rgba(56,189,248,0.25)] flex items-center justify-center p-4 group hover:scale-105 transition-transform duration-300">
            <!-- Official TuronBank Emblem Logo -->
            <TuronBankIcon
              :size="84"
              primary-color="#1d4ed8"
              secondary-color="#38bdf8"
              wave-color="#ffffff"
              glow-color="#38bdf8"
              :show-glow="true"
              id="ai-center-logo"
            />
          </div>

          <!-- 4 Database Nodes (ATM, MONITOR, FILIAL, SERVIS) -->
          <div class="absolute top-2 left-4 px-2 py-0.5 rounded bg-slate-900/90 border border-slate-800 text-[9px] font-mono text-sky-400 flex items-center gap-1 shadow">
            <Database class="w-3 h-3 text-sky-400" /> DB • ATM
          </div>

          <div class="absolute top-2 right-4 px-2 py-0.5 rounded bg-slate-900/90 border border-slate-800 text-[9px] font-mono text-indigo-400 flex items-center gap-1 shadow">
            <Database class="w-3 h-3 text-indigo-400" /> DB • MONITOR
          </div>

          <div class="absolute bottom-2 left-4 px-2 py-0.5 rounded bg-slate-900/90 border border-slate-800 text-[9px] font-mono text-emerald-400 flex items-center gap-1 shadow">
            <Database class="w-3 h-3 text-emerald-400" /> DB • FILIAL
          </div>

          <div class="absolute bottom-2 right-4 px-2 py-0.5 rounded bg-slate-900/90 border border-slate-800 text-[9px] font-mono text-purple-400 flex items-center gap-1 shadow">
            <Database class="w-3 h-3 text-purple-400" /> DB • SERVIS
          </div>
        </div>
      </div>

      <!-- Right Column: 4 AI Cards -->
      <div class="lg:col-span-4 space-y-3.5">
        <!-- 5. AI Prognoz (SOON) -->
        <div class="flex items-center justify-between p-3.5 rounded-2xl bg-slate-900/60 border border-slate-800/80 opacity-90 transition-all group">
          <div class="flex items-center gap-3 min-w-0">
            <div class="p-2.5 rounded-xl bg-blue-500/10 text-blue-400 border border-blue-500/20 shrink-0">
              <TrendingUp class="w-5 h-5" />
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-slate-200 truncate">AI Prognoz</span>
                <span class="px-2 py-0.2 rounded-full text-[9px] font-black bg-amber-500/10 text-amber-400 border border-amber-500/30">SOON</span>
              </div>
              <p class="text-[11px] text-slate-400 truncate mt-0.5">Keyingi oy uchun moliyaviy prognoz</p>
            </div>
          </div>
        </div>

        <!-- 6. AI Filiallar (SOON) -->
        <div class="flex items-center justify-between p-3.5 rounded-2xl bg-slate-900/60 border border-slate-800/80 opacity-90 transition-all group">
          <div class="flex items-center gap-3 min-w-0">
            <div class="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 shrink-0">
              <Building2 class="w-5 h-5" />
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-slate-200 truncate">AI Filiallar</span>
                <span class="px-2 py-0.2 rounded-full text-[9px] font-black bg-amber-500/10 text-amber-400 border border-amber-500/30">SOON</span>
              </div>
              <p class="text-[11px] text-slate-400 truncate mt-0.5">Filiallar aylanmasi bo'yicha AI tahlil</p>
            </div>
          </div>
        </div>

        <!-- 7. AI Trend Tahlili (SOON) -->
        <div class="flex items-center justify-between p-3.5 rounded-2xl bg-slate-900/60 border border-slate-800/80 opacity-90 transition-all group">
          <div class="flex items-center gap-3 min-w-0">
            <div class="p-2.5 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/20 shrink-0">
              <LineChart class="w-5 h-5" />
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-slate-200 truncate">AI Trend Tahlili</span>
                <span class="px-2 py-0.2 rounded-full text-[9px] font-black bg-amber-500/10 text-amber-400 border border-amber-500/30">SOON</span>
              </div>
              <p class="text-[11px] text-slate-400 truncate mt-0.5">Daromad va xarajat trendlarini AI aniqlaydi</p>
            </div>
          </div>
        </div>

        <!-- 8. AI Texnik Holat (SOON) -->
        <div class="flex items-center justify-between p-3.5 rounded-2xl bg-slate-900/60 border border-slate-800/80 opacity-90 transition-all group">
          <div class="flex items-center gap-3 min-w-0">
            <div class="p-2.5 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20 shrink-0">
              <Wrench class="w-5 h-5" />
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-slate-200 truncate">AI Texnik Holat</span>
                <span class="px-2 py-0.2 rounded-full text-[9px] font-black bg-amber-500/10 text-amber-400 border border-amber-500/30">SOON</span>
              </div>
              <p class="text-[11px] text-slate-400 truncate mt-0.5">ATM texnik holatini bashorat qilish</p>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- Bottom Action Pill Buttons -->
    <div class="flex flex-wrap items-center justify-center gap-3 relative z-10 pt-2">
      <button
        @click="$emit('selectTab', 'ai-studio')"
        class="px-6 py-2.5 rounded-full bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-extrabold text-xs shadow-lg shadow-indigo-500/25 border border-blue-400/30 transition-all cursor-pointer active:scale-95 flex items-center gap-2"
      >
        <Sparkles class="w-4 h-4" />
        <span>AI xizmatlar</span>
      </button>

      <button
        @click="$emit('selectTab', 'regions')"
        class="px-6 py-2.5 rounded-full bg-slate-900 hover:bg-slate-800 text-sky-300 font-extrabold text-xs border border-slate-800 hover:border-sky-500/40 transition-all cursor-pointer active:scale-95 flex items-center gap-2"
      >
        <Building2 class="w-4 h-4" />
        <span>Filiallar bo'yicha</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import TuronBankIcon from '@/components/common/TuronBankIcon.vue';
import {
  Sparkles,
  ShieldAlert,
  AlertOctagon,
  Wallet,
  TrendingUp,
  Building2,
  LineChart,
  Wrench,
  Database
} from 'lucide-vue-next';

defineEmits<{
  (e: 'selectTab', tab: string): void;
}>();
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
'''

hub_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\AiBankomatPortalHub.vue'
with open(hub_path, 'w', encoding='utf-8') as f:
    f.write(hub_component_code)

print("AiBankomatPortalHub.vue created successfully!")
