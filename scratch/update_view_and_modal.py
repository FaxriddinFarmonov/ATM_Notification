import os

# 1. Update EngineersView.vue to import and render AssignAtmModal
engineers_view_code = '''<template>
  <div class="space-y-6 pb-12 animate-fade-in">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white dark:bg-slate-800/90 p-6 rounded-2xl border border-slate-200 dark:border-slate-700/60 shadow-sm">
      <div>
        <div class="flex items-center gap-3">
          <div class="p-3 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 rounded-xl">
            <Users class="w-7 h-7" />
          </div>
          <div>
            <h1 class="text-xl font-bold text-slate-900 dark:text-white tracking-tight">
              Texnik Muhandislar Boshqaruvi
            </h1>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              Bankomatlarga biriktirilgan texniklar, ularning hududlari va holati
            </p>
          </div>
        </div>
      </div>

      <!-- Header actions: Refresh & Add Engineer -->
      <div class="flex items-center gap-2">
        <button
          @click="store.fetchEngineers()"
          :disabled="store.loading"
          class="px-3.5 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-700 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-200 text-xs font-semibold transition-all flex items-center gap-2"
          title="Ma'lumotlarni yangilash"
        >
          <RefreshCw :class="{ 'animate-spin': store.loading }" class="w-4 h-4 text-emerald-500" />
          <span>Yangilash</span>
        </button>

        <button
          @click="store.openCreateModal()"
          class="px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition-all shadow-md hover:shadow-lg flex items-center gap-2"
        >
          <UserPlus class="w-4 h-4" />
          <span>Yangi Muhandis Yaratish</span>
        </button>
      </div>
    </div>

    <!-- Top Overview KPI Stats Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="bg-white dark:bg-slate-800/90 p-5 rounded-2xl border border-slate-200 dark:border-slate-700/60 shadow-sm flex items-center gap-4">
        <div class="p-3.5 rounded-2xl bg-sky-500/10 text-sky-600 dark:text-sky-400">
          <Users class="w-6 h-6" />
        </div>
        <div>
          <span class="text-xs text-slate-500 dark:text-slate-400 font-medium">Jami Muhandislar</span>
          <p class="text-xl font-bold text-slate-900 dark:text-white mt-0.5">{{ store.totalEngineersCount }} nafar</p>
        </div>
      </div>

      <div class="bg-white dark:bg-slate-800/90 p-5 rounded-2xl border border-slate-200 dark:border-slate-700/60 shadow-sm flex items-center gap-4">
        <div class="p-3.5 rounded-2xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
          <HardDrive class="w-6 h-6" />
        </div>
        <div>
          <span class="text-xs text-slate-500 dark:text-slate-400 font-medium">Biriktirilgan ATMlar</span>
          <p class="text-xl font-bold text-slate-900 dark:text-white mt-0.5">{{ store.totalAssignedAtmsCount }} ta</p>
        </div>
      </div>

      <div class="bg-white dark:bg-slate-800/90 p-5 rounded-2xl border border-slate-200 dark:border-slate-700/60 shadow-sm flex items-center gap-4">
        <div class="p-3.5 rounded-2xl bg-teal-500/10 text-teal-600 dark:text-teal-400">
          <ShieldCheck class="w-6 h-6" />
        </div>
        <div>
          <span class="text-xs text-slate-500 dark:text-slate-400 font-medium">Soz (InService)</span>
          <p class="text-xl font-bold text-emerald-600 dark:text-emerald-400 mt-0.5">{{ store.totalInServiceCount }} ta</p>
        </div>
      </div>

      <div class="bg-white dark:bg-slate-800/90 p-5 rounded-2xl border border-slate-200 dark:border-slate-700/60 shadow-sm flex items-center gap-4">
        <div class="p-3.5 rounded-2xl bg-amber-500/10 text-amber-600 dark:text-amber-400">
          <Coins class="w-6 h-6" />
        </div>
        <div>
          <span class="text-xs text-slate-500 dark:text-slate-400 font-medium">Boshqarilayotgan Naqd</span>
          <p class="text-xl font-bold text-slate-900 dark:text-white mt-0.5">{{ formatBillion(store.totalCashManaged) }}</p>
        </div>
      </div>
    </div>

    <!-- Search & Region Filter Toolbar -->
    <div class="bg-white dark:bg-slate-800/90 p-4 rounded-2xl border border-slate-200 dark:border-slate-700/60 shadow-sm flex flex-col md:flex-row gap-3 items-center justify-between">
      <!-- Search Input -->
      <div class="relative w-full md:w-96">
        <Search class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
        <input
          v-model="store.searchQuery"
          type="text"
          placeholder="Ism, sharif, telefon yoki mutaxassislik..."
          class="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-700 text-xs text-slate-800 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all"
        />
        <button
          v-if="store.searchQuery"
          @click="store.searchQuery = ''"
          class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
        >
          <X class="w-3.5 h-3.5" />
        </button>
      </div>

      <!-- Region Filter -->
      <div class="flex items-center gap-2 w-full md:w-auto overflow-x-auto">
        <span class="text-xs text-slate-500 dark:text-slate-400 whitespace-nowrap font-medium">Hudud:</span>
        <select
          v-model="store.selectedRegion"
          class="py-2 px-3 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-700 text-xs text-slate-800 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500"
        >
          <option value="all">Barcha hududlar</option>
          <option v-for="reg in store.uniqueRegions" :key="reg" :value="reg">
            {{ reg }}
          </option>
        </select>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="store.loading && store.engineers.length === 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="i in 6" :key="i" class="h-64 bg-slate-100 dark:bg-slate-800/50 rounded-2xl animate-pulse"></div>
    </div>

    <!-- Engineers Cards Grid -->
    <div v-else-if="store.filteredEngineers.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="eng in store.filteredEngineers"
        :key="eng.id"
        class="bg-white dark:bg-slate-800/90 rounded-2xl border border-slate-200 dark:border-slate-700/60 p-5 hover:border-emerald-500/50 hover:shadow-xl transition-all duration-300 flex flex-col justify-between gap-4 group relative overflow-hidden"
      >
        <!-- Top accent line -->
        <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-emerald-500 to-teal-500 opacity-80 group-hover:opacity-100 transition-opacity"></div>

        <div>
          <!-- Header: Avatar + Region -->
          <div class="flex items-start justify-between gap-3">
            <div class="relative">
              <img
                v-if="eng.avatar_url"
                :src="eng.avatar_url"
                :alt="eng.full_name"
                class="w-14 h-14 rounded-2xl object-cover border-2 border-emerald-500/40 shadow-md group-hover:scale-105 transition-transform"
              />
              <div
                v-else
                class="w-14 h-14 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-700 flex items-center justify-center text-white font-bold text-lg border-2 border-emerald-500/40 shadow-md"
              >
                {{ getInitials(eng.full_name) }}
              </div>
              <span class="absolute -bottom-1 -right-1 w-4 h-4 bg-emerald-500 border-2 border-white dark:border-slate-800 rounded-full"></span>
            </div>

            <!-- ATMs Count Badge -->
            <div class="text-right">
              <span class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-bold bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
                <HardDrive class="w-3.5 h-3.5" />
                {{ eng.assigned_atms_count }} ta ATM
              </span>
            </div>
          </div>

          <!-- Name & Specialization -->
          <div class="mt-4">
            <h3 class="font-bold text-slate-900 dark:text-white text-base tracking-tight group-hover:text-emerald-500 transition-colors">
              {{ eng.full_name }}
            </h3>
            <p v-if="eng.patronymic" class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              Sharifi: <span class="font-medium text-slate-700 dark:text-slate-300">{{ eng.patronymic }}</span>
            </p>
            <p class="text-xs text-emerald-600 dark:text-emerald-400 font-semibold mt-1">
              {{ eng.specialization }}
            </p>
          </div>

          <!-- Region badge -->
          <div class="mt-2.5 flex items-center gap-1.5 text-xs text-slate-500 dark:text-slate-400">
            <MapPin class="w-3.5 h-3.5 text-slate-400 shrink-0" />
            <span class="line-clamp-1">{{ eng.region }}</span>
          </div>

          <!-- Contact buttons: Telegram & Phone -->
          <div class="mt-4 pt-3.5 border-t border-slate-100 dark:border-slate-700/60 space-y-2">
            <!-- Telegram button -->
            <a
              v-if="eng.telegram_username"
              :href="`https://t.me/${eng.telegram_username}`"
              target="_blank"
              rel="noopener noreferrer"
              class="flex items-center justify-between px-3 py-2 rounded-xl bg-sky-50 hover:bg-sky-100 dark:bg-sky-950/40 dark:hover:bg-sky-900/50 text-sky-700 dark:text-sky-300 border border-sky-200 dark:border-sky-800/60 text-xs font-semibold transition-all group/tg"
              title="Telegramda xabar yuborish"
            >
              <span class="flex items-center gap-2">
                <Send class="w-3.5 h-3.5 text-sky-500 group-hover/tg:translate-x-0.5 transition-transform" />
                <span>@{{ eng.telegram_username }}</span>
              </span>
              <ExternalLink class="w-3 h-3 opacity-60" />
            </a>

            <!-- Phone button -->
            <a
              v-if="eng.phone"
              :href="`tel:${eng.phone}`"
              class="flex items-center justify-between px-3 py-2 rounded-xl bg-emerald-50 hover:bg-emerald-100 dark:bg-emerald-950/40 dark:hover:bg-emerald-900/50 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/60 text-xs font-semibold transition-all"
              title="Qo'ng'iroq qilish"
            >
              <span class="flex items-center gap-2">
                <Phone class="w-3.5 h-3.5 text-emerald-500" />
                <span>{{ eng.phone }}</span>
              </span>
              <PhoneCall class="w-3 h-3 opacity-60" />
            </a>
          </div>

          <!-- Status stats: InService / OutOfService -->
          <div class="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-slate-100 dark:border-slate-700/60 text-xs">
            <div class="bg-emerald-50/70 dark:bg-emerald-950/30 rounded-lg p-2 text-center border border-emerald-200/50 dark:border-emerald-800/40">
              <span class="text-slate-500 dark:text-slate-400 block text-[10px]">Faol (InService)</span>
              <span class="font-bold text-emerald-600 dark:text-emerald-400 text-sm">{{ eng.in_service_count }}</span>
            </div>
            <div class="bg-red-50/70 dark:bg-red-950/30 rounded-lg p-2 text-center border border-red-200/50 dark:border-red-800/40">
              <span class="text-slate-500 dark:text-slate-400 block text-[10px]">Nosoz</span>
              <span class="font-bold text-red-600 dark:text-red-400 text-sm">{{ eng.out_of_service_count }}</span>
            </div>
          </div>
        </div>

        <!-- Card Main Action: View ATMs -->
        <button
          @click="store.openEngineerDetail(eng.id)"
          class="w-full py-2.5 px-4 rounded-xl bg-slate-900 hover:bg-emerald-600 dark:bg-slate-700 dark:hover:bg-emerald-600 text-white text-xs font-bold transition-all duration-200 flex items-center justify-center gap-2 shadow-sm group-hover:shadow-md group-hover:scale-[1.02]"
        >
          <span>Bankomatlarni ko'rish ({{ eng.assigned_atms_count }})</span>
          <ArrowRight class="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
        </button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="p-16 text-center bg-white dark:bg-slate-800/90 rounded-2xl border border-slate-200 dark:border-slate-700/60">
      <Users class="w-12 h-12 text-slate-400 mx-auto mb-3 opacity-40" />
      <h3 class="text-base font-bold text-slate-800 dark:text-white">Mos muhandislar topilmadi</h3>
      <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">Qidiruv yoki hudud filtrini tozalab ko'ring</p>
      <button
        @click="store.searchQuery = ''; store.selectedRegion = 'all'"
        class="mt-4 px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold transition-colors"
      >
        Filtrlarni tozalash
      </button>
    </div>

    <!-- Modals -->
    <EngineerDetailModal />
    <CreateEngineerModal />
    <AssignAtmModal />
    <BTechAtmDetailModal />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useEngineerStore } from '@/stores/engineerStore';
import { useBtechStore } from '@/stores/btechStore';
import EngineerDetailModal from '@/components/engineers/EngineerDetailModal.vue';
import CreateEngineerModal from '@/components/engineers/CreateEngineerModal.vue';
import AssignAtmModal from '@/components/engineers/AssignAtmModal.vue';
import BTechAtmDetailModal from '@/components/btech/BTechAtmDetailModal.vue';
import {
  Users,
  HardDrive,
  Coins,
  ShieldCheck,
  RefreshCw,
  UserPlus,
  Search,
  X,
  MapPin,
  Send,
  Phone,
  PhoneCall,
  ExternalLink,
  ArrowRight,
} from 'lucide-vue-next';

const store = useEngineerStore();
const btechStore = useBtechStore();

onMounted(async () => {
  store.fetchEngineers();
  if (btechStore.atms.length === 0) {
    btechStore.fetchAtms();
  }
});

function getInitials(name: string) {
  if (!name) return 'TM';
  const parts = name.split(' ').filter(Boolean);
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }
  return name.slice(0, 2).toUpperCase();
}

function formatBillion(num: number) {
  if (!num) return "0 so'm";
  const billions = num / 1_000_000_000;
  return `${billions.toFixed(2)} mlrd UZS`;
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

with open(r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\views\EngineersView.vue', 'w', encoding='utf-8') as f:
    f.write(engineers_view_code)

print("Updated EngineersView.vue successfully!")
