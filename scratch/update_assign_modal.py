import os

assign_modal_code = '''<template>
  <Teleport to="body">
    <div
      v-if="isOpen"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/70 backdrop-blur-md animate-fade-in"
    >
      <div
        class="bg-white dark:bg-slate-900 w-full max-w-3xl rounded-3xl shadow-2xl border border-slate-200 dark:border-slate-800 flex flex-col max-h-[85vh] overflow-hidden"
        @click.stop
      >
        <!-- Header -->
        <div class="p-6 bg-slate-900 text-white flex items-center justify-between relative overflow-hidden">
          <div class="absolute -right-10 -bottom-10 w-40 h-40 bg-emerald-500/10 rounded-full blur-2xl pointer-events-none"></div>

          <div>
            <div class="flex items-center gap-2">
              <HardDrive class="w-6 h-6 text-emerald-400" />
              <h2 class="text-lg font-bold">Bankomat Biriktirish</h2>
            </div>
            <p class="text-xs text-slate-400 mt-1">
              Muhandis: <span class="text-emerald-400 font-semibold">{{ targetEngineerName }}</span>
            </p>
          </div>

          <button
            @click="closeModal"
            class="p-2 rounded-xl bg-white/10 hover:bg-white/20 text-slate-300 hover:text-white transition-colors"
          >
            <X class="w-5 h-5" />
          </button>
        </div>

        <!-- Search Bar -->
        <div class="p-4 bg-slate-50 dark:bg-slate-800/50 border-b border-slate-200 dark:border-slate-800 flex items-center gap-3">
          <div class="relative flex-1">
            <Search class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              v-model="searchQuery"
              @input="handleSearch"
              type="text"
              placeholder="Bankomat Serial, TID, Filial yoki Manzil bo'yicha qidirish..."
              class="w-full pl-10 pr-4 py-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs text-slate-800 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
            <button
              v-if="searchQuery"
              @click="searchQuery = ''; handleSearch()"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
            >
              <X class="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        <!-- ATM List -->
        <div class="flex-1 overflow-y-auto p-4 space-y-3">
          <div v-if="loading" class="p-12 text-center text-slate-400 text-xs">
            <RefreshCw class="w-6 h-6 animate-spin mx-auto mb-2 text-emerald-500" />
            Bankomatlar ro'yxati yuklanmoqda...
          </div>

          <div v-else-if="atms.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div
              v-for="atm in atms"
              :key="atm.serial"
              class="p-4 rounded-2xl border transition-all duration-200 flex flex-col justify-between gap-3 bg-white dark:bg-slate-800/80 border-slate-200 dark:border-slate-700/60 hover:border-emerald-500/40 hover:shadow-md"
            >
              <div>
                <div class="flex items-start justify-between gap-2">
                  <div class="flex items-center gap-2">
                    <div class="p-2 rounded-xl bg-emerald-500/10 text-emerald-500">
                      <HardDrive class="w-4 h-4" />
                    </div>
                    <div>
                      <div class="flex items-center gap-2">
                        <span class="font-bold text-slate-900 dark:text-white text-sm">{{ atm.serial }}</span>
                        <span class="text-[10px] px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-700 font-mono text-slate-600 dark:text-slate-300">
                          TID: {{ atm.tid || '---' }}
                        </span>
                      </div>
                      <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
                        {{ atm.model_name }} • Filial: {{ atm.branch_number || '---' }}
                      </p>
                    </div>
                  </div>
                </div>

                <p class="text-xs text-slate-600 dark:text-slate-300 mt-2 flex items-start gap-1 line-clamp-2">
                  <MapPin class="w-3.5 h-3.5 text-slate-400 shrink-0 mt-0.5" />
                  <span>{{ atm.address || 'Manzil ko\'rsatilmagan' }}</span>
                </p>

                <!-- Current Engineer Badge -->
                <div class="mt-2.5 pt-2 border-t border-slate-100 dark:border-slate-700/50 text-[11px]">
                  <span v-if="atm.responsible_engineer_id === targetEngineerId" class="text-emerald-600 dark:text-emerald-400 font-bold flex items-center gap-1">
                    <CheckCircle2 class="w-3.5 h-3.5" /> Ushbu muhandisga biriktirilgan
                  </span>
                  <span v-else-if="atm.responsible_engineer_name" class="text-amber-600 dark:text-amber-400 font-medium flex items-center gap-1">
                    <UserCheck class="w-3.5 h-3.5" /> Hozirgi: {{ atm.responsible_engineer_name }}
                  </span>
                  <span v-else class="text-slate-400 flex items-center gap-1">
                    <HelpCircle class="w-3.5 h-3.5" /> Biriktirilmagan (Bo'sh)
                  </span>
                </div>
              </div>

              <!-- Assign Action Button -->
              <div>
                <button
                  v-if="atm.responsible_engineer_id === targetEngineerId"
                  disabled
                  class="w-full py-2 px-3 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 text-xs font-semibold border border-emerald-200 dark:border-emerald-800 flex items-center justify-center gap-1.5 opacity-80 cursor-default"
                >
                  <CheckCircle2 class="w-4 h-4" />
                  <span>Biriktirilgan</span>
                </button>

                <button
                  v-else-if="atm.responsible_engineer_name"
                  @click="assign(atm)"
                  :disabled="assigningSerial === atm.serial"
                  class="w-full py-2 px-3 rounded-xl bg-amber-500 hover:bg-amber-600 text-white text-xs font-bold transition-all shadow-sm flex items-center justify-center gap-1.5 active:scale-[0.98]"
                >
                  <RefreshCw v-if="assigningSerial === atm.serial" class="w-3.5 h-3.5 animate-spin" />
                  <ArrowRightLeft v-else class="w-3.5 h-3.5" />
                  <span>O'tkazish (Almashtirish)</span>
                </button>

                <button
                  v-else
                  @click="assign(atm)"
                  :disabled="assigningSerial === atm.serial"
                  class="w-full py-2 px-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition-all shadow-sm flex items-center justify-center gap-1.5 active:scale-[0.98]"
                >
                  <RefreshCw v-if="assigningSerial === atm.serial" class="w-3.5 h-3.5 animate-spin" />
                  <Plus v-else class="w-3.5 h-3.5" />
                  <span>Biriktirish</span>
                </button>
              </div>
            </div>
          </div>

          <div v-else class="p-12 text-center bg-slate-50 dark:bg-slate-800/40 rounded-2xl">
            <HardDrive class="w-10 h-10 text-slate-400 mx-auto mb-2 opacity-40" />
            <p class="text-xs font-semibold text-slate-700 dark:text-slate-300">Bankomatlar topilmadi</p>
            <p class="text-[11px] text-slate-400 mt-0.5">Boshqa seriya yoki kalit so'z bilan qidirib ko'ring</p>
          </div>
        </div>

        <!-- Footer -->
        <div class="p-4 bg-slate-50 dark:bg-slate-800/60 border-t border-slate-200 dark:border-slate-800 flex justify-end">
          <button
            @click="closeModal"
            class="px-5 py-2 rounded-xl bg-slate-200 hover:bg-slate-300 dark:bg-slate-700 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-200 text-xs font-bold transition-colors"
          >
            Yopish
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue';
import { useEngineerStore } from '@/stores/engineerStore';
import { engineerService, type AvailableATMItem } from '@/services/engineerService';
import {
  X,
  Search,
  HardDrive,
  MapPin,
  CheckCircle2,
  UserCheck,
  HelpCircle,
  Plus,
  ArrowRightLeft,
  RefreshCw
} from 'lucide-vue-next';

const store = useEngineerStore();

const isOpen = computed(() => store.isAssignAtmModalOpen);
const targetEngineerId = computed(() => store.selectedEngineer?.id || 0);
const targetEngineerName = computed(() => store.selectedEngineer?.full_name || 'Muhandis');

const searchQuery = ref('');
const loading = ref(false);
const atms = ref<AvailableATMItem[]>([]);
const assigningSerial = ref<string | null>(null);

let debounceTimer: any = null;

watch(isOpen, async (val) => {
  if (val) {
    searchQuery.value = '';
    await loadAtms();
  }
});

async function loadAtms() {
  loading.value = true;
  try {
    const data = await engineerService.getAvailableAtms(searchQuery.value);
    atms.value = data;
  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
}

function handleSearch() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    loadAtms();
  }, 300);
}

async function assign(atm: AvailableATMItem) {
  if (!targetEngineerId.value) return;

  if (atm.responsible_engineer_name && atm.responsible_engineer_id !== targetEngineerId.value) {
    if (!confirm(`Ushbu ${atm.serial} bankomat ${atm.responsible_engineer_name}dan ${targetEngineerName.value}ga o'tkazilsinmi?`)) {
      return;
    }
  }

  assigningSerial.value = atm.serial;
  try {
    await store.assignAtm(targetEngineerId.value, atm.serial, atm.tid);
    await loadAtms();
  } catch (err) {
    alert('Bankomat biriktirishda xatolik yuz berdi.');
  } finally {
    assigningSerial.value = null;
  }
}

function closeModal() {
  store.closeAssignAtmModal();
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

with open(r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\engineers\AssignAtmModal.vue', 'w', encoding='utf-8') as f:
    f.write(assign_modal_code)

print("Created AssignAtmModal.vue successfully!")
