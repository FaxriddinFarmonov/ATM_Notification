import os

engineers_code = '''<template>
  <div class="space-y-6 pb-12 animate-fade-in">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl text-white">
      <div>
        <div class="flex items-center gap-3">
          <div class="p-3 bg-emerald-500/10 text-emerald-400 rounded-xl border border-emerald-500/20">
            <Users class="w-7 h-7" />
          </div>
          <div>
            <h1 class="text-xl font-bold text-white tracking-tight">
              Texnik Muhandislar Boshqaruvi
            </h1>
            <p class="text-xs text-slate-400 mt-0.5">
              Bankomatlarga biriktirilgan texniklar, ularning hududlari va operatsion holati
            </p>
          </div>
        </div>
      </div>

      <!-- Header actions: Refresh & Add Engineer -->
      <div class="flex items-center gap-3">
        <button
          @click="store.fetchEngineers()"
          :disabled="store.loading"
          class="px-3.5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition-all flex items-center gap-2 border border-slate-700 cursor-pointer"
          title="Ma'lumotlarni yangilash"
        >
          <RefreshCw :class="{ 'animate-spin': store.loading }" class="w-4 h-4 text-emerald-400" />
          <span>Yangilash</span>
        </button>

        <button
          @click="store.openCreateModal()"
          class="px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition-all shadow-lg shadow-emerald-600/20 flex items-center gap-2 border border-emerald-500/30 cursor-pointer"
        >
          <UserPlus class="w-4 h-4" />
          <span>Yangi Muhandis Yaratish</span>
        </button>
      </div>
    </div>

    <!-- Top Overview KPI Stats Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="bg-slate-900 p-5 rounded-2xl border border-slate-800 shadow-md flex items-center gap-4">
        <div class="p-3.5 rounded-2xl bg-sky-500/10 text-sky-400 border border-sky-500/20">
          <Users class="w-6 h-6" />
        </div>
        <div>
          <span class="text-xs text-slate-400 font-medium">Jami Muhandislar</span>
          <p class="text-xl font-black text-white mt-0.5">{{ store.totalEngineersCount }} nafar</p>
        </div>
      </div>

      <div class="bg-slate-900 p-5 rounded-2xl border border-slate-800 shadow-md flex items-center gap-4">
        <div class="p-3.5 rounded-2xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <HardDrive class="w-6 h-6" />
        </div>
        <div>
          <span class="text-xs text-slate-400 font-medium">Biriktirilgan ATMlar</span>
          <p class="text-xl font-black text-white mt-0.5">{{ store.totalAssignedAtmsCount }} ta</p>
        </div>
      </div>

      <div class="bg-slate-900 p-5 rounded-2xl border border-slate-800 shadow-md flex items-center gap-4">
        <div class="p-3.5 rounded-2xl bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
          <ShieldCheck class="w-6 h-6" />
        </div>
        <div>
          <span class="text-xs text-slate-400 font-medium">Faol ATMlar (InService)</span>
          <p class="text-xl font-black text-emerald-400 mt-0.5">{{ store.totalInServiceCount }} ta</p>
        </div>
      </div>

      <div class="bg-slate-900 p-5 rounded-2xl border border-slate-800 shadow-md flex items-center gap-4">
        <div class="p-3.5 rounded-2xl bg-rose-500/10 text-rose-400 border border-rose-500/20">
          <Coins class="w-6 h-6" />
        </div>
        <div>
          <span class="text-xs text-slate-400 font-medium">Nosoz ATMlar</span>
          <p class="text-xl font-black text-rose-400 mt-0.5">{{ store.totalOutOfServiceCount }} ta</p>
        </div>
      </div>
    </div>

    <!-- Controls Bar: Search, Region Filter & Layout Switcher -->
    <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4 bg-slate-900 p-4 rounded-2xl border border-slate-800">
      <!-- Search input -->
      <div class="relative flex-1 max-w-md">
        <Search class="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
        <input
          v-model="store.searchQuery"
          type="text"
          placeholder="Ism, sharif, telefon yoki mutaxassislik..."
          class="w-full pl-10 pr-9 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white text-xs placeholder:text-slate-500 focus:outline-none focus:border-emerald-500 transition-colors"
        />
        <button
          v-if="store.searchQuery"
          @click="store.searchQuery = ''"
          class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white"
        >
          <X class="w-4 h-4" />
        </button>
      </div>

      <!-- Region Select & View Switcher -->
      <div class="flex items-center gap-3">
        <div class="flex items-center gap-2 text-xs text-slate-400 font-medium">
          <span class="hidden sm:inline">Hudud:</span>
          <select
            v-model="store.selectedRegion"
            class="px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white text-xs font-semibold focus:outline-none focus:border-emerald-500 transition-colors cursor-pointer"
          >
            <option value="all" class="bg-slate-900 text-slate-100">Barcha hududlar</option>
            <option
              v-for="region in store.uniqueRegions"
              :key="region"
              :value="region"
              class="bg-slate-900 text-slate-100"
            >
              {{ region }}
            </option>
          </select>
        </div>

        <!-- Layout Mode Toggle (Table / Grid) -->
        <div class="flex items-center p-1 bg-slate-950 rounded-xl border border-slate-800">
          <button
            @click="viewMode = 'table'"
            :class="[
              'p-2 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 cursor-pointer',
              viewMode === 'table'
                ? 'bg-emerald-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-white'
            ]"
            title="Jadval ko'rinishi"
          >
            <Table class="w-4 h-4" />
            <span class="hidden md:inline">Jadval</span>
          </button>
          <button
            @click="viewMode = 'grid'"
            :class="[
              'p-2 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 cursor-pointer',
              viewMode === 'grid'
                ? 'bg-emerald-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-white'
            ]"
            title="Karta ko'rinishi"
          >
            <LayoutGrid class="w-4 h-4" />
            <span class="hidden md:inline">Karta</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="store.loading && store.engineers.length === 0" class="flex flex-col items-center justify-center py-20 bg-slate-900 rounded-2xl border border-slate-800">
      <div class="w-8 h-8 border-3 border-emerald-400 border-t-transparent rounded-full animate-spin mb-3"></div>
      <p class="text-sm font-bold text-slate-300">Texnik muhandislar ro'yxati yuklanmoqda...</p>
    </div>

    <!-- Main Content Container: Table View or Grid View -->
    <template v-else-if="store.filteredEngineers.length > 0">
      <!-- 1. Executive Senior Table View (Default) -->
      <div v-if="viewMode === 'table'" class="bg-slate-900 rounded-2xl border border-slate-800 shadow-xl overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-xs text-left">
            <thead class="bg-slate-950 text-slate-400 font-extrabold uppercase tracking-wider border-b border-slate-800">
              <tr>
                <th class="p-4">Muhandis / Texnik</th>
                <th class="p-4">Hudud</th>
                <th class="p-4">Aloqa (Telefon / Telegram)</th>
                <th class="p-4 text-center">ATMlar Soni</th>
                <th class="p-4 text-center">Faol (InService)</th>
                <th class="p-4 text-center">Nosoz</th>
                <th class="p-4 text-right">Amal</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800 font-medium">
              <tr
                v-for="eng in store.filteredEngineers"
                :key="eng.id"
                class="hover:bg-slate-800/50 transition-colors group"
              >
                <!-- Avatar & Name -->
                <td class="p-4">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 font-black text-sm flex items-center justify-center shrink-0">
                      {{ getInitials(eng.full_name) }}
                    </div>
                    <div class="min-w-0">
                      <p class="font-bold text-white text-sm tracking-tight group-hover:text-emerald-400 transition-colors truncate">
                        {{ eng.full_name }}
                      </p>
                      <p v-if="eng.patronymic" class="text-[11px] text-slate-400 truncate mt-0.5">
                        Sharifi: <span class="text-slate-300 font-semibold">{{ eng.patronymic }}</span>
                      </p>
                      <span class="inline-block mt-1 px-2 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-emerald-400 border border-slate-700">
                        {{ eng.specialization || 'ATM Servis Muhandisi' }}
                      </span>
                    </div>
                  </div>
                </td>

                <!-- Region -->
                <td class="p-4">
                  <div class="flex items-center gap-1.5 text-slate-300">
                    <MapPin class="w-3.5 h-3.5 text-slate-400 shrink-0" />
                    <span class="font-semibold">{{ eng.region }}</span>
                  </div>
                </td>

                <!-- Contact -->
                <td class="p-4">
                  <div class="space-y-1">
                    <a
                      v-if="eng.phone"
                      :href="`tel:${eng.phone}`"
                      class="inline-flex items-center gap-1.5 text-emerald-400 hover:text-emerald-300 font-bold hover:underline"
                    >
                      <Phone class="w-3.5 h-3.5" />
                      <span>{{ eng.phone }}</span>
                    </a>
                    <div v-if="eng.telegram_username" class="text-[11px] text-sky-400 flex items-center gap-1 font-semibold">
                      <Send class="w-3 h-3" />
                      <span>@{{ eng.telegram_username }}</span>
                    </div>
                  </div>
                </td>

                <!-- Assigned ATMs Count -->
                <td class="p-4 text-center">
                  <span class="px-3 py-1 rounded-full text-xs font-black bg-sky-500/10 text-sky-300 border border-sky-500/20 inline-flex items-center gap-1">
                    <HardDrive class="w-3.5 h-3.5" />
                    {{ eng.assigned_atms_count }} ta ATM
                  </span>
                </td>

                <!-- InService Count -->
                <td class="p-4 text-center">
                  <span class="px-2.5 py-1 rounded-md text-xs font-extrabold bg-emerald-950/60 text-emerald-300 border border-emerald-800">
                    {{ eng.in_service_count }}
                  </span>
                </td>

                <!-- OutOfService Count -->
                <td class="p-4 text-center">
                  <span
                    class="px-2.5 py-1 rounded-md text-xs font-extrabold border"
                    :class="eng.out_of_service_count > 0 ? 'bg-rose-950/60 text-rose-300 border-rose-800' : 'bg-slate-800 text-slate-400 border-slate-700'"
                  >
                    {{ eng.out_of_service_count }}
                  </span>
                </td>

                <!-- Action button -->
                <td class="p-4 text-right">
                  <button
                    @click="store.openEngineerDetail(eng.id)"
                    class="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-emerald-600 text-white font-bold text-xs transition-all inline-flex items-center gap-1.5 border border-slate-700 hover:border-emerald-500 cursor-pointer shadow-sm"
                  >
                    <span>Bankomatlar ({{ eng.assigned_atms_count }})</span>
                    <ArrowRight class="w-3.5 h-3.5" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 2. Grid Cards View -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        <div
          v-for="eng in store.filteredEngineers"
          :key="eng.id"
          class="bg-slate-900 rounded-2xl p-5 border border-slate-800 shadow-lg hover:border-slate-700 transition-all flex flex-col justify-between group"
        >
          <div>
            <!-- Card Header: Initials + Assigned ATMs badge -->
            <div class="flex items-start justify-between gap-3">
              <div class="w-12 h-12 rounded-2xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 font-black text-base flex items-center justify-center shrink-0">
                {{ getInitials(eng.full_name) }}
              </div>

              <!-- ATMs Count Badge -->
              <div class="text-right">
                <span class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-bold bg-emerald-950/60 text-emerald-300 border border-emerald-800">
                  <HardDrive class="w-3.5 h-3.5" />
                  {{ eng.assigned_atms_count }} ta ATM
                </span>
              </div>
            </div>

            <!-- Name & Specialization -->
            <div class="mt-4">
              <h3 class="font-bold text-white text-base tracking-tight group-hover:text-emerald-400 transition-colors">
                {{ eng.full_name }}
              </h3>
              <p v-if="eng.patronymic" class="text-xs text-slate-400 mt-0.5">
                Sharifi: <span class="font-medium text-slate-300">{{ eng.patronymic }}</span>
              </p>
              <p class="text-xs text-emerald-400 font-semibold mt-1">
                {{ eng.specialization || 'ATM Servis Muhandisi' }}
              </p>
            </div>

            <!-- Region badge -->
            <div class="mt-2.5 flex items-center gap-1.5 text-xs text-slate-400">
              <MapPin class="w-3.5 h-3.5 text-slate-400 shrink-0" />
              <span class="line-clamp-1">{{ eng.region }}</span>
            </div>

            <!-- Contact buttons: Telegram & Phone -->
            <div class="mt-4 pt-3.5 border-t border-slate-800 space-y-2">
              <!-- Telegram button -->
              <a
                v-if="eng.telegram_username"
                :href="`https://t.me/${eng.telegram_username}`"
                target="_blank"
                rel="noopener noreferrer"
                class="flex items-center justify-between px-3 py-2 rounded-xl bg-sky-950/40 hover:bg-sky-900/50 text-sky-300 border border-sky-800/60 text-xs font-semibold transition-all group/tg"
                title="Telegramda xabar yuborish"
              >
                <span class="flex items-center gap-2">
                  <Send class="w-3.5 h-3.5 text-sky-400 group-hover/tg:translate-x-0.5 transition-transform" />
                  <span>@{{ eng.telegram_username }}</span>
                </span>
                <ExternalLink class="w-3 h-3 opacity-60" />
              </a>

              <!-- Phone button -->
              <a
                v-if="eng.phone"
                :href="`tel:${eng.phone}`"
                class="flex items-center justify-between px-3 py-2 rounded-xl bg-emerald-950/40 hover:bg-emerald-900/50 text-emerald-300 border border-emerald-800/60 text-xs font-semibold transition-all"
                title="Qo'ng'iroq qilish"
              >
                <span class="flex items-center gap-2">
                  <Phone class="w-3.5 h-3.5 text-emerald-400" />
                  <span>{{ eng.phone }}</span>
                </span>
                <PhoneCall class="w-3 h-3 opacity-60" />
              </a>
            </div>

            <!-- Status stats: InService / OutOfService -->
            <div class="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-slate-800 text-xs">
              <div class="bg-emerald-950/30 rounded-lg p-2 text-center border border-emerald-800/40">
                <span class="text-slate-400 block text-[10px]">Faol (InService)</span>
                <span class="font-bold text-emerald-400 text-sm">{{ eng.in_service_count }}</span>
              </div>
              <div class="bg-rose-950/30 rounded-lg p-2 text-center border border-rose-800/40">
                <span class="text-slate-400 block text-[10px]">Nosoz</span>
                <span class="font-bold text-rose-400 text-sm">{{ eng.out_of_service_count }}</span>
              </div>
            </div>
          </div>

          <!-- Card Main Action: View ATMs -->
          <button
            @click="store.openEngineerDetail(eng.id)"
            class="w-full mt-4 py-2.5 px-4 rounded-xl bg-slate-800 hover:bg-emerald-600 text-white text-xs font-bold transition-all duration-200 flex items-center justify-center gap-2 shadow-sm border border-slate-700 cursor-pointer"
          >
            <span>Bankomatlarni ko'rish ({{ eng.assigned_atms_count }})</span>
            <ArrowRight class="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
      </div>
    </template>

    <!-- Empty State -->
    <div v-else class="p-16 text-center bg-slate-900 rounded-2xl border border-slate-800">
      <Users class="w-12 h-12 text-slate-500 mx-auto mb-3 opacity-50" />
      <h3 class="text-base font-bold text-white">Mos muhandislar topilmadi</h3>
      <p class="text-xs text-slate-400 mt-1">Qidiruv yoki hudud filtrini tozalab ko'ring</p>
      <button
        @click="store.searchQuery = ''; store.selectedRegion = 'all'"
        class="mt-4 px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold transition-colors cursor-pointer"
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
import { ref, onMounted } from 'vue';
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
  Table,
  LayoutGrid
} from 'lucide-vue-next';

const store = useEngineerStore();
const btechStore = useBtechStore();

// Default layout mode: Table View
const viewMode = ref<'table' | 'grid'>('table');

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

target_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\views\EngineersView.vue'
with open(target_path, 'w', encoding='utf-8') as f:
    f.write(engineers_code)

print("EngineersView.vue updated successfully!")
