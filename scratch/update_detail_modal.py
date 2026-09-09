import os

detail_modal_code = '''<template>
  <Teleport to="body">
    <div
      v-if="store.isDetailModalOpen"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/70 backdrop-blur-md animate-fade-in"
    >
      <div
        class="bg-white dark:bg-slate-900 w-full max-w-5xl rounded-3xl shadow-2xl border border-slate-200 dark:border-slate-800 flex flex-col max-h-[90vh] overflow-hidden"
        @click.stop
      >
        <!-- Loading state -->
        <div v-if="store.detailLoading" class="p-16 text-center text-slate-400">
          <div class="w-10 h-10 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p class="text-sm font-semibold text-slate-700 dark:text-slate-200">Muhandis ma'lumotlari va bankomatlar yuklanmoqda...</p>
        </div>

        <template v-else-if="engineer">
          <!-- Modal Header Banner -->
          <div class="relative bg-gradient-to-r from-slate-900 via-slate-800 to-teal-950 p-6 text-white overflow-hidden shrink-0">
            <!-- Background accent glow -->
            <div class="absolute -right-12 -top-12 w-48 h-48 bg-emerald-500/20 rounded-full blur-3xl pointer-events-none"></div>

            <div class="flex items-start justify-between gap-4 relative z-10">
              <div class="flex items-center gap-4">
                <img
                  v-if="engineer.avatar_url"
                  :src="engineer.avatar_url"
                  :alt="engineer.full_name"
                  class="w-16 h-16 rounded-2xl object-cover border-2 border-emerald-400/50 shadow-lg"
                />
                <div
                  v-else
                  class="w-16 h-16 rounded-2xl bg-gradient-to-tr from-emerald-500 to-teal-600 flex items-center justify-center text-white font-bold text-xl border-2 border-emerald-400/50 shadow-lg"
                >
                  {{ getInitials(engineer.full_name) }}
                </div>

                <div>
                  <div class="flex items-center gap-2">
                    <h2 class="text-xl font-bold tracking-tight text-white">{{ engineer.full_name }}</h2>
                    <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                      {{ engineer.region || 'Barcha hududlar' }}
                    </span>
                  </div>
                  <p class="text-xs text-emerald-400 font-medium mt-0.5">{{ engineer.specialization }}</p>

                  <div class="flex flex-wrap items-center gap-4 mt-2 text-xs text-slate-300">
                    <span v-if="engineer.phone" class="flex items-center gap-1.5">
                      <Phone class="w-3.5 h-3.5 text-emerald-400" />
                      {{ engineer.phone }}
                    </span>
                    <a
                      v-if="engineer.telegram_username"
                      :href="`https://t.me/${engineer.telegram_username}`"
                      target="_blank"
                      class="flex items-center gap-1.5 text-sky-300 hover:underline"
                    >
                      <Send class="w-3.5 h-3.5 text-sky-400" />
                      @{{ engineer.telegram_username }}
                    </a>
                  </div>
                </div>
              </div>

              <button
                @click="store.closeDetailModal"
                class="p-2 rounded-xl bg-white/10 hover:bg-white/20 text-slate-300 hover:text-white transition-colors"
              >
                <X class="w-5 h-5" />
              </button>
            </div>

            <!-- Mini stats bar -->
            <div class="grid grid-cols-4 gap-3 mt-5 pt-4 border-t border-white/10 text-xs">
              <div>
                <span class="text-slate-400 text-[10px] block">Jami Bankomatlar</span>
                <span class="font-bold text-white text-base">{{ engineer.assigned_atms_count }} ta</span>
              </div>
              <div>
                <span class="text-slate-400 text-[10px] block">Faol (InService)</span>
                <span class="font-bold text-emerald-400 text-base">{{ engineer.in_service_count }} ta</span>
              </div>
              <div>
                <span class="text-slate-400 text-[10px] block">Nosoz</span>
                <span class="font-bold text-red-400 text-base">{{ engineer.out_of_service_count }} ta</span>
              </div>
              <div>
                <span class="text-slate-400 text-[10px] block">Umumiy Pul Qoldig'i</span>
                <span class="font-bold text-teal-300 text-base">{{ formatAmount(engineer.total_cash) }}</span>
              </div>
            </div>
          </div>

          <!-- Controls Bar: Search + Filter + Add ATM Button -->
          <div class="p-4 bg-slate-50 dark:bg-slate-800/50 border-b border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-3 shrink-0">
            <div class="flex items-center gap-2 w-full sm:w-auto flex-1">
              <div class="relative flex-1 max-w-sm">
                <Search class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  v-model="atmSearchQuery"
                  type="text"
                  placeholder="Serial, TID, Manzil bo'yicha qidirish..."
                  class="w-full pl-9 pr-3 py-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs text-slate-800 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>

              <!-- Status filter -->
              <select
                v-model="statusFilter"
                class="py-2 px-3 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs text-slate-800 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option value="all">Barchasi ({{ engineer.atms ? engineer.atms.length : 0 }})</option>
                <option value="inservice">Soz (InService)</option>
                <option value="outofservice">Nosoz (OutOfService)</option>
              </select>
            </div>

            <!-- Primary Action: Assign ATM Button -->
            <button
              @click="store.openAssignAtmModal()"
              class="w-full sm:w-auto px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition-all shadow-md hover:shadow-lg flex items-center justify-center gap-2"
            >
              <Plus class="w-4 h-4" />
              <span>+ Bankomat Biriktirish</span>
            </button>
          </div>

          <!-- ATMs List Grid -->
          <div class="flex-1 overflow-y-auto p-6">
            <div v-if="filteredAtms.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div
                v-for="atm in filteredAtms"
                :key="atm.serial"
                class="bg-white dark:bg-slate-800/90 border border-slate-200 dark:border-slate-700/70 rounded-xl p-4 hover:border-emerald-500/50 hover:shadow-md transition-all duration-200 flex flex-col justify-between gap-3 group"
              >
                <!-- Card Header -->
                <div>
                  <div class="flex items-start justify-between gap-2">
                    <div class="flex items-center gap-2">
                      <div
                        :class="atm.service_status === 'InService' ? 'bg-emerald-500/15 text-emerald-600 dark:text-emerald-400' : 'bg-red-500/15 text-red-600 dark:text-red-400'"
                        class="p-2 rounded-lg"
                      >
                        <HardDrive class="w-5 h-5" />
                      </div>
                      <div>
                        <div class="flex items-center gap-2">
                          <span class="font-bold text-slate-900 dark:text-white text-base tracking-wide">{{ atm.serial }}</span>
                          <span class="text-xs px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-700 font-mono text-slate-600 dark:text-slate-300">
                            TID: {{ atm.tid || '---' }}
                          </span>
                        </div>
                        <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                          {{ atm.model_name }} • Filial: {{ atm.branch_number || '---' }}
                        </p>
                      </div>
                    </div>

                    <!-- Status Badge -->
                    <span
                      :class="atm.service_status === 'InService' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800' : 'bg-red-100 text-red-800 dark:bg-red-950/60 dark:text-red-300 border-red-200 dark:border-red-800'"
                      class="px-2.5 py-1 rounded-full text-xs font-semibold border flex items-center gap-1.5"
                    >
                      <span
                        :class="atm.service_status === 'InService' ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'"
                        class="w-1.5 h-1.5 rounded-full"
                      ></span>
                      {{ atm.service_status }}
                    </span>
                  </div>

                  <!-- Address -->
                  <p class="text-xs text-slate-600 dark:text-slate-300 mt-3 flex items-start gap-1.5 line-clamp-2">
                    <MapPin class="w-3.5 h-3.5 text-slate-400 shrink-0 mt-0.5" />
                    <span>{{ atm.address || 'Manzil ko\'rsatilmagan' }}</span>
                  </p>
                </div>

                <!-- Footer details -->
                <div class="pt-3 border-t border-slate-100 dark:border-slate-700/60 flex items-center justify-between text-xs">
                  <div>
                    <span class="text-slate-500 dark:text-slate-400">Kasseta qoldig'i:</span>
                    <p class="font-bold text-emerald-600 dark:text-emerald-400 text-sm">
                      {{ formatAmount(atm.cash_amount) }}
                    </p>
                  </div>

                  <div class="flex items-center gap-1.5">
                    <!-- View hardware details button -->
                    <button
                      @click="openBtechModalForAtm(atm.serial)"
                      class="px-2.5 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-slate-700 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-200 text-xs font-medium transition-colors flex items-center gap-1"
                      title="BTech apparat telemetriyasini ko'rish"
                    >
                      <Activity class="w-3.5 h-3.5 text-emerald-500" />
                      Pasport
                    </button>

                    <!-- Unassign button -->
                    <button
                      @click="confirmUnassign(atm.serial)"
                      class="px-2 py-1.5 rounded-lg text-red-600 bg-red-50 hover:bg-red-100 dark:bg-red-950/40 dark:hover:bg-red-900/50 text-xs font-semibold border border-red-200 dark:border-red-800/60 transition-colors flex items-center gap-1"
                      title="Muhandisdan ajratish (Olib tashlash)"
                    >
                      <Trash2 class="w-3.5 h-3.5" />
                      <span>Ajratish</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Empty state if no ATMs match filter -->
            <div v-else class="p-12 text-center bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700/60">
              <HardDrive class="w-10 h-10 text-slate-400 mx-auto mb-2 opacity-50" />
              <p class="text-slate-600 dark:text-slate-300 font-medium">Ushbu muhandisga biriktirilgan bankomatlar topilmadi</p>
              <p class="text-xs text-slate-400 mt-1">"Bankomat Biriktirish" tugmasini bosib, yangi bankomat biriktirishingiz mumkin</p>
              <button
                @click="store.openAssignAtmModal()"
                class="mt-4 px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition-colors inline-flex items-center gap-2"
              >
                <Plus class="w-4 h-4" />
                <span>Hozir Biriktirish</span>
              </button>
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="p-4 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between">
            <div class="text-xs text-slate-500 dark:text-slate-400 flex items-center gap-2">
              <ShieldCheck class="w-4 h-4 text-emerald-500" />
              <span>Turonbank ATM Monitoring & Telemetriya Xizmati</span>
            </div>

            <button
              @click="store.closeDetailModal"
              class="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-xs font-semibold transition-colors"
            >
              Yopish
            </button>
          </div>
        </template>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useEngineerStore } from '@/stores/engineerStore';
import { useBtechStore } from '@/stores/btechStore';
import {
  X,
  Phone,
  Send,
  Search,
  HardDrive,
  MapPin,
  Activity,
  Trash2,
  ShieldCheck,
  Plus
} from 'lucide-vue-next';

const store = useEngineerStore();
const btechStore = useBtechStore();

const engineer = computed(() => store.selectedEngineer);

const atmSearchQuery = ref('');
const statusFilter = ref<'all' | 'inservice' | 'outofservice'>('all');

const filteredAtms = computed(() => {
  if (!engineer.value || !engineer.value.atms) return [];
  return engineer.value.atms.filter((atm) => {
    // Status filter
    if (statusFilter.value === 'inservice' && atm.service_status !== 'InService') {
      return false;
    }
    if (statusFilter.value === 'outofservice' && atm.service_status === 'InService') {
      return false;
    }

    // Search query
    if (atmSearchQuery.value.trim()) {
      const q = atmSearchQuery.value.toLowerCase().trim();
      const match =
        atm.serial.toLowerCase().includes(q) ||
        atm.tid.toLowerCase().includes(q) ||
        atm.address.toLowerCase().includes(q) ||
        atm.model_name.toLowerCase().includes(q) ||
        atm.branch_number.toLowerCase().includes(q);
      if (!match) return false;
    }

    return true;
  });
});

function getInitials(name: string) {
  if (!name) return 'TM';
  const parts = name.split(' ').filter(Boolean);
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }
  return name.slice(0, 2).toUpperCase();
}

function formatAmount(num: number) {
  if (!num) return "0 so'm";
  return new Intl.NumberFormat('uz-UZ').format(num) + " so'm";
}

function confirmUnassign(serial: string) {
  if (confirm(`Rostdan ham ${serial} seriyali bankomatni ushbu muhandisdan ajratmoqchimisiz?`)) {
    store.unassignAtm(serial);
  }
}

function openBtechModalForAtm(serial: string) {
  const item = btechStore.atms.find((a: any) => a.serial === serial);
  if (item) {
    btechStore.openDetailModal(item);
  } else {
    alert(`Bankomat ${serial} haqida BTech telemetriyasi yuklanmoqda...`);
  }
}
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.2s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.98); }
  to { opacity: 1; transform: scale(1); }
}
</style>
'''

with open(r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\engineers\EngineerDetailModal.vue', 'w', encoding='utf-8') as f:
    f.write(detail_modal_code)

print("Updated EngineerDetailModal.vue successfully!")
