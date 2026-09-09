import os

modal_code = '''<template>
  <Teleport to="body">
    <Transition name="atm-modal">
      <div
        v-if="open"
        class="fixed inset-0 z-[100] flex items-center justify-center p-3 sm:p-6 bg-slate-950/80 backdrop-blur-md"
        role="dialog"
        aria-modal="true"
        @click.self="close"
      >
        <!-- Full-Width Executive Screen Modal Container (max-w-7xl / 95vw) -->
        <div
          id="atm-detail-pdf-report"
          class="w-full max-w-[95vw] lg:max-w-7xl max-h-[92vh] bg-slate-900 border border-slate-800 rounded-3xl shadow-2xl text-white flex flex-col overflow-hidden"
        >
          <!-- Modal Header -->
          <div class="flex items-center justify-between gap-4 px-6 py-5 border-b border-slate-800 bg-slate-950/60 flex-shrink-0">
            <div class="flex items-center gap-4 min-w-0">
              <div class="p-3.5 rounded-2xl bg-blue-500/10 text-blue-400 border border-blue-500/20 flex-shrink-0">
                <Landmark class="w-7 h-7" />
              </div>
              <div class="min-w-0">
                <div class="flex items-center gap-2.5 flex-wrap">
                  <span class="text-xs font-black text-sky-400 uppercase tracking-widest">TURONBANK ATB</span>
                  <span class="w-1.5 h-1.5 rounded-full bg-slate-600"></span>
                  <span
                    v-if="detail?.technical?.status"
                    class="px-2.5 py-0.5 rounded-full text-xs font-bold border inline-flex items-center gap-1.5"
                    :class="[
                      detail.technical.status === 'soz' || detail.technical.status === 'active'
                        ? 'bg-emerald-950/60 text-emerald-300 border-emerald-800'
                        : 'bg-rose-950/60 text-rose-300 border-rose-800'
                    ]"
                  >
                    <span :class="['w-1.5 h-1.5 rounded-full', detail.technical.status === 'soz' || detail.technical.status === 'active' ? 'bg-emerald-400' : 'bg-rose-400']"></span>
                    {{ statusToLabel(detail.technical.status) }}
                  </span>
                </div>
                <h2 class="text-xl sm:text-2xl font-black text-white truncate mt-0.5" :title="detail?.general.name ?? ''">
                  {{ detail?.general.name || fallbackName || "ATM Ma'lumoti" }}
                </h2>
                <p v-if="detail" class="text-xs text-slate-400 truncate font-medium">
                  {{ detail.general.region }} • {{ detail.general.address || "Manzil ko'rsatilmagan" }}
                </p>
              </div>
            </div>

            <!-- Action Toolbar (PDF Export & Close) -->
            <div class="flex items-center gap-3">
              <button
                v-if="detail"
                type="button"
                @click="exportPdf"
                :disabled="isExporting"
                class="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-red-600 via-rose-600 to-pink-600 hover:from-red-500 hover:to-pink-500 text-white font-extrabold text-xs shadow-lg shadow-red-500/25 border border-red-400/40 transition-all active:scale-95 disabled:opacity-50 cursor-pointer"
              >
                <Download class="w-4 h-4" />
                <span>{{ isExporting ? 'PDF Yasalmoqda...' : 'Download PDF' }}</span>
              </button>

              <button
                type="button"
                class="p-2.5 rounded-2xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors cursor-pointer"
                aria-label="Yopish"
                @click="close"
              >
                <X class="w-5 h-5" />
              </button>
            </div>
          </div>

          <!-- Scrollable Modal Body -->
          <div id="atm-detail-scroll-body" class="flex-1 overflow-y-auto px-6 py-6 space-y-6 custom-scroll">
            <!-- Loading State -->
            <div v-if="atmStore.isDetailLoading && !detail" class="flex flex-col items-center justify-center py-20">
              <div class="w-8 h-8 border-3 border-blue-400 border-t-transparent rounded-full animate-spin mb-3"></div>
              <p class="text-sm font-bold text-slate-300">Bankomat ma'lumotlari yuklanmoqda...</p>
            </div>

            <!-- Error State -->
            <div v-else-if="atmStore.detailError && !detail" class="flex flex-col items-center justify-center py-16 text-center">
              <div class="w-12 h-12 rounded-2xl bg-rose-500/10 text-rose-400 flex items-center justify-center mb-3">
                <AlertCircle class="w-6 h-6" />
              </div>
              <p class="text-sm font-bold text-white">Ma'lumotni yuklab bo'lmadi</p>
              <p class="text-xs text-slate-400 mt-1">{{ atmStore.detailError }}</p>
              <button
                type="button"
                class="mt-4 px-4 py-2 text-xs font-bold bg-blue-600 hover:bg-blue-500 text-white rounded-xl transition-colors"
                @click="retry"
              >
                Qayta urinish
              </button>
            </div>

            <div v-else-if="detail" class="space-y-6">
              <!-- Technical, General & Comprehensive Service Expense Cards Grid -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <!-- General Info -->
                <div class="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-3">
                  <div class="flex items-center gap-2 text-xs font-bold text-sky-400 uppercase tracking-wider">
                    <Info class="w-4 h-4" />
                    <span>Umumiy Ma'lumot</span>
                  </div>
                  <div class="space-y-2 divide-y divide-slate-800/60">
                    <InfoRow label="Viloyat / Filial" :value="detail.general.region" />
                    <InfoRow label="Manzil" :value="detail.general.address" />
                    <InfoRow label="Model" :value="detail.general.model" mono />
                    <div class="flex items-center justify-between pt-2 text-xs font-semibold">
                      <span class="text-slate-400">Karta turi</span>
                      <span
                        v-if="detail.general.card_type"
                        class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-blue-500/15 text-sky-300 border border-blue-500/30"
                      >
                        {{ detail.general.card_type }}
                      </span>
                      <span v-else class="text-slate-500">---</span>
                    </div>
                  </div>
                </div>

                <!-- Technical Telemetry -->
                <div class="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-3">
                  <div class="flex items-center gap-2 text-xs font-bold text-indigo-400 uppercase tracking-wider">
                    <Cpu class="w-4 h-4" />
                    <span>Texnik Telemetriya</span>
                  </div>
                  <div class="space-y-2 divide-y divide-slate-800/60">
                    <InfoRow label="Terminal ID (TID)" :value="detail.technical.terminal_id" mono />
                    <InfoRow label="Merchant ID" :value="detail.technical.merchant_id" mono />
                    <InfoRow label="Seriya raqami" :value="detail.technical.serial_number" mono />
                    <InfoRow label="Inventar №" :value="detail.technical.inventory_number" mono />
                  </div>
                </div>

                <!-- Comprehensive Operational Expenses & Service Contract -->
                <div class="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-3">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-2 text-xs font-bold text-emerald-400 uppercase tracking-wider">
                      <FileText class="w-4 h-4" />
                      <span>Servis & Operatsion Xarajatlar</span>
                    </div>
                    <span v-if="totalOperationalFee > 0" class="text-[11px] font-black text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-md border border-emerald-500/20">
                      {{ formatUzSum(totalOperationalFee) }}/oy
                    </span>
                  </div>
                  <div class="grid grid-cols-2 gap-2 pt-1">
                    <div class="p-2.5 bg-slate-900 rounded-xl border border-slate-800">
                      <p class="text-[10px] text-slate-400 font-bold uppercase">BTech oylik</p>
                      <p class="text-xs font-black text-emerald-400 tabular-nums mt-0.5">
                        {{ formatUzSum(detail.service_contract?.btech_monthly_fee) }}
                      </p>
                    </div>
                    <div class="p-2.5 bg-slate-900 rounded-xl border border-slate-800">
                      <p class="text-[10px] text-slate-400 font-bold uppercase">Glob oylik</p>
                      <p class="text-xs font-black text-sky-400 tabular-nums mt-0.5">
                        {{ formatUzSum(detail.service_contract?.glob_monthly_fee) }}
                      </p>
                    </div>
                    <div class="p-2.5 bg-slate-900 rounded-xl border border-slate-800">
                      <p class="text-[10px] text-slate-400 font-bold uppercase">Elektr to'lovi</p>
                      <p class="text-xs font-black text-amber-400 tabular-nums mt-0.5">
                        {{ formatUzSum(electricityFee) }}
                      </p>
                    </div>
                    <div class="p-2.5 bg-slate-900 rounded-xl border border-slate-800">
                      <p class="text-[10px] text-slate-400 font-bold uppercase">Ijara to'lovi</p>
                      <p class="text-xs font-black text-indigo-400 tabular-nums mt-0.5">
                        {{ formatUzSum(rentFee) }}
                      </p>
                    </div>
                    <div class="p-2.5 bg-slate-900 rounded-xl border border-slate-800 col-span-2 flex items-center justify-between">
                      <p class="text-[10px] text-slate-400 font-bold uppercase">Inkassatsiya sarfi</p>
                      <p class="text-xs font-black text-rose-400 tabular-nums">
                        {{ formatUzSum(incassationFee) }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Executive Line Chart ONLY for Income (Daromad) -->
              <div v-if="monthlyStats.length > 0" class="p-6 rounded-2xl bg-slate-950/90 border border-slate-800 space-y-4">
                <div class="flex items-center justify-between flex-wrap gap-2">
                  <div>
                    <h3 class="text-base font-extrabold text-white flex items-center gap-2">
                      <span class="w-3 h-3 rounded-full bg-sky-400"></span>
                      Oylik Daromad Dinamikasi (Kirim)
                    </h3>
                    <p class="text-xs text-slate-400 mt-0.5">Faqat tushgan daromadlar grafikasi ({{ monthlyRange }})</p>
                  </div>
                  <div class="flex items-center gap-3 text-xs font-bold">
                    <span class="flex items-center gap-1.5 text-sky-400">
                      <span class="w-3 h-3 rounded-sm bg-sky-400"></span> Daromad (Mln UZS)
                    </span>
                  </div>
                </div>

                <!-- Smooth Line Chart for Income Only -->
                <div class="h-72">
                  <DualAxisChart :data="incomeLineChartData" y-axis-unit="Mln UZS" />
                </div>
              </div>

              <!-- Yearly Statistics Table -->
              <div v-if="yearlyStats.length > 0" class="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-3">
                <h3 class="text-sm font-bold text-white uppercase tracking-wider">Yillik Statistika</h3>
                <div class="overflow-x-auto rounded-xl border border-slate-800">
                  <table class="w-full text-xs text-left">
                    <thead class="bg-slate-900 text-slate-400 font-extrabold uppercase border-b border-slate-800">
                      <tr>
                        <th class="p-3">Yil</th>
                        <th class="p-3 text-center">Karta Turi</th>
                        <th class="p-3 text-right">Kirim (Daromad)</th>
                        <th class="p-3 text-right">Chiqim (Aylanma)</th>
                        <th class="p-3 text-right">Ta'mirlash Sarfi</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-800 font-medium">
                      <tr v-for="y in yearlyStats" :key="`${y.year}-${y.card_type}`" class="hover:bg-slate-900/60 transition-colors">
                        <td class="p-3 font-bold text-white text-sm">{{ y.year }}</td>
                        <td class="p-3 text-center">
                          <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-blue-500/15 text-sky-300 border border-blue-500/30">
                            {{ y.card_type }}
                          </span>
                        </td>
                        <td class="p-3 text-right font-bold text-sky-400 text-sm">{{ formatUzSum(y.income) }}</td>
                        <td class="p-3 text-right font-bold text-slate-200 text-sm">{{ formatUzSum(y.expense) }}</td>
                        <td class="p-3 text-right font-bold text-rose-400 text-sm">{{ formatUzSum(y.repair_cost) }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- Detailed Monthly Statistics Table -->
              <div v-if="monthlyStats.length > 0" class="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-3">
                <h3 class="text-sm font-bold text-white uppercase tracking-wider">Oylar Kesimida Batafsil Statistika</h3>
                <div id="pdf-monthly-table-container" class="overflow-x-auto rounded-xl border border-slate-800 max-h-96 custom-scroll">
                  <table class="w-full text-xs text-left">
                    <thead class="bg-slate-900 text-slate-400 font-extrabold uppercase border-b border-slate-800 sticky top-0">
                      <tr>
                        <th class="p-3">Oy</th>
                        <th class="p-3 text-right">Kirim (Daromad)</th>
                        <th class="p-3 text-right">Chiqim (Naqd Aylanma)</th>
                        <th class="p-3 text-right">Ta'mirlash Sarfi</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-800 font-medium">
                      <tr v-for="m in monthlyStats" :key="`${m.year}-${m.month}`" class="hover:bg-slate-900/60 transition-colors">
                        <td class="p-3 font-bold text-white">{{ monthLabel(m.year, m.month) }}</td>
                        <td class="p-3 text-right font-bold text-sky-400 text-sm">{{ formatUzSum(m.income) }}</td>
                        <td class="p-3 text-right font-bold text-slate-200 text-sm">{{ formatUzSum(m.expense) }}</td>
                        <td class="p-3 text-right font-bold text-rose-400 text-sm">{{ formatUzSum(m.repair_cost) }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, h, onBeforeUnmount, watch, ref } from 'vue';
import { Landmark, X, AlertCircle, Info, Cpu, FileText, Download } from 'lucide-vue-next';
import { useAtmStore } from '@/stores/atmStore';
import { statusToLabel } from '@/types';
import { monthKeyToLabel } from '@/utils/chartMappers';
import DualAxisChart from '@/components/charts/DualAxisChart.vue';
import type { BarLineChartData } from '@/types/api';
import html2canvas from 'html2canvas';
import { jsPDF } from 'jspdf';

const props = defineProps<{
  open: boolean;
  atmId: number | null;
  fallbackName?: string | null;
}>();

const emit = defineEmits<{
  (e: 'update:open', value: boolean): void;
}>();

const atmStore = useAtmStore();
const isExporting = ref(false);

const detail = computed(() => {
  if (props.atmId == null) return null;
  return atmStore.detailCache.get(props.atmId) ?? null;
});

const monthlyStats = computed(() => {
  const stats = detail.value?.monthly_statistics ?? [];
  return [...stats].sort((a, b) => a.year - b.year || a.month - b.month);
});

const yearlyStats = computed(() => detail.value?.yearly_statistics ?? []);

const serviceContract = computed(() => detail.value?.service_contract ?? null);

const electricityFee = computed(() => {
  const payments = serviceContract.value?.payments ?? [];
  const item = payments.find(p => p.payment_type?.toUpperCase() === 'ELECTRICITY');
  return item?.amount || 0;
});

const rentFee = computed(() => {
  const payments = serviceContract.value?.payments ?? [];
  const item = payments.find(p => p.payment_type?.toUpperCase() === 'RENT');
  return item?.amount || 0;
});

const incassationFee = computed(() => {
  const payments = serviceContract.value?.payments ?? [];
  const item = payments.find(p => p.payment_type?.toUpperCase() === 'INCASSATION');
  return item?.amount || 0;
});

const totalOperationalFee = computed(() => {
  const btech = serviceContract.value?.btech_monthly_fee || 0;
  const glob = serviceContract.value?.glob_monthly_fee || 0;
  return btech + glob + electricityFee.value + rentFee.value + incassationFee.value;
});

function monthLabel(year: number, month: number): string {
  return monthKeyToLabel(`${year}-${String(month).padStart(2, '0')}`);
}

function formatUzSum(val: number | null | undefined): string {
  if (val === undefined || val === null || isNaN(val) || val === 0) return "0 so'm";
  const abs = Math.abs(val);
  if (abs >= 1_000_000_000_000) return (val / 1_000_000_000_000).toFixed(2) + " Trln so'm";
  if (abs >= 1_000_000_000) return (val / 1_000_000_000).toFixed(2) + " Mlrd so'm";
  if (abs >= 1_000_000) return (val / 1_000_000).toFixed(2) + " Mln so'm";
  if (abs >= 1_000) return (val / 1_000).toFixed(1) + " MING so'm";
  return val.toLocaleString('uz-UZ') + " so'm";
}

// Line Chart ONLY for Income (Daromad/Kirim)
const incomeLineChartData = computed<BarLineChartData>(() => ({
  labels: monthlyStats.value.map((m) => monthLabel(m.year, m.month)),
  datasets: [
    {
      type: 'line',
      label: 'Daromad (Mln UZS)',
      data: monthlyStats.value.map((m) => +((m.income || 0) / 1_000_000).toFixed(2)),
      borderColor: '#38bdf8',
      backgroundColor: 'rgba(56, 189, 248, 0.15)',
      pointBackgroundColor: '#38bdf8',
      pointRadius: 4,
      pointHoverRadius: 7,
      tension: 0.35,
      fill: true,
      borderWidth: 3
    }
  ]
}));

const monthlyRange = computed(() => {
  if (monthlyStats.value.length === 0) return '';
  const first = monthlyStats.value[0];
  const last = monthlyStats.value[monthlyStats.value.length - 1];
  return `${monthLabel(first.year, first.month)} — ${monthLabel(last.year, last.month)}`;
});

const InfoRow = (props: { label: string; value: string | number | null | undefined; mono?: boolean }) => {
  return h('div', { class: 'flex items-center justify-between py-1.5 text-xs gap-3 font-medium' }, [
    h('span', { class: 'text-slate-400 flex-shrink-0' }, props.label),
    h(
      'span',
      {
        class: [
          'text-white font-bold text-right truncate',
          props.mono ? 'font-mono text-sky-400' : ''
        ].join(' '),
        title: props.value != null ? String(props.value) : ''
      },
      props.value !== null && props.value !== undefined && props.value !== '' ? String(props.value) : '---'
    )
  ]);
};

async function exportPdf() {
  if (isExporting.value || !detail.value) return;
  isExporting.value = true;
  try {
    const reportElement = document.getElementById('atm-detail-pdf-report');
    const scrollBody = document.getElementById('atm-detail-scroll-body');
    const tableContainer = document.getElementById('pdf-monthly-table-container');

    if (!reportElement) {
      console.error("PDF Report element not found!");
      return;
    }

    // Save current styling
    const origReportMaxHeight = reportElement.style.maxHeight;
    const origReportOverflow = reportElement.style.overflow;
    const origBodyMaxHeight = scrollBody?.style.maxHeight || '';
    const origBodyOverflow = scrollBody?.style.overflow || '';
    const origTableMaxHeight = tableContainer?.style.maxHeight || '';
    const origTableOverflow = tableContainer?.style.overflow || '';

    // Expand element fully in live DOM for html2canvas capture!
    reportElement.style.maxHeight = 'none';
    reportElement.style.overflow = 'visible';
    if (scrollBody) {
      scrollBody.style.maxHeight = 'none';
      scrollBody.style.overflow = 'visible';
    }
    if (tableContainer) {
      tableContainer.style.maxHeight = 'none';
      tableContainer.style.overflow = 'visible';
    }

    await new Promise(r => setTimeout(r, 150));

    const canvas = await html2canvas(reportElement, {
      scale: 2,
      useCORS: true,
      backgroundColor: '#020617',
      logging: false,
      windowWidth: document.documentElement.offsetWidth
    });

    // Restore original styles immediately
    reportElement.style.maxHeight = origReportMaxHeight;
    reportElement.style.overflow = origReportOverflow;
    if (scrollBody) {
      scrollBody.style.maxHeight = origBodyMaxHeight;
      scrollBody.style.overflow = origBodyOverflow;
    }
    if (tableContainer) {
      tableContainer.style.maxHeight = origTableMaxHeight;
      tableContainer.style.overflow = origTableOverflow;
    }

    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4'
    });

    const pdfWidth = 210; // A4 mm
    const pdfHeight = 297; // A4 mm
    const margin = 8;
    const printWidth = pdfWidth - (margin * 2); // 194 mm
    const printHeight = (canvas.height * printWidth) / canvas.width;

    let heightLeft = printHeight;
    let position = margin;

    // First Page
    pdf.setFillColor(2, 6, 23);
    pdf.rect(0, 0, pdfWidth, pdfHeight, 'F');
    pdf.addImage(imgData, 'PNG', margin, position, printWidth, printHeight);
    heightLeft -= (pdfHeight - (margin * 2));

    // Subsequent Pages if content exceeds page 1
    while (heightLeft > 0) {
      position = position - (pdfHeight - (margin * 2));
      pdf.addPage();
      pdf.setFillColor(2, 6, 23);
      pdf.rect(0, 0, pdfWidth, pdfHeight, 'F');
      pdf.addImage(imgData, 'PNG', margin, position, printWidth, printHeight);
      heightLeft -= (pdfHeight - (margin * 2));
    }

    const tid = detail.value.technical?.terminal_id || 'ATM';
    pdf.save(`Turonbank_ATM_Pasport_${tid}.pdf`);
  } catch (err) {
    console.error("ATM PDF export error:", err);
    alert("PDF saqlashda xatolik yuz berdi: " + (err instanceof Error ? err.message : String(err)));
  } finally {
    isExporting.value = false;
  }
}

function close(): void {
  emit('update:open', false);
}

function retry(): void {
  if (props.atmId == null) return;
  atmStore.fetchAtmDetail(props.atmId, true);
}

function onKeydown(event: KeyboardEvent): void {
  if (event.key === 'Escape' && props.open) {
    event.preventDefault();
    close();
  }
}

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      window.addEventListener('keydown', onKeydown);
      if (props.atmId != null && !atmStore.detailCache.has(props.atmId)) {
        atmStore.fetchAtmDetail(props.atmId);
      }
    } else {
      document.body.style.overflow = '';
      window.removeEventListener('keydown', onKeydown);
    }
  }
);

onBeforeUnmount(() => {
  document.body.style.overflow = '';
  window.removeEventListener('keydown', onKeydown);
});
</script>

<style scoped>
.custom-scroll {
  scrollbar-width: thin;
  scrollbar-color: rgba(56, 189, 248, 0.3) transparent;
}
.custom-scroll::-webkit-scrollbar {
  width: 6px;
}
.custom-scroll::-webkit-scrollbar-thumb {
  background: rgba(56, 189, 248, 0.3);
  border-radius: 9999px;
}

.atm-modal-enter-active,
.atm-modal-leave-active {
  transition: opacity 0.18s ease;
}
.atm-modal-enter-active > div,
.atm-modal-leave-active > div {
  transition: transform 0.22s ease, opacity 0.18s ease;
}
.atm-modal-enter-from,
.atm-modal-leave-to {
  opacity: 0;
}
.atm-modal-enter-from > div,
.atm-modal-leave-to > div {
  transform: translateY(12px) scale(0.98);
  opacity: 0;
}
</style>
'''

target_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\monitoring\AtmDetailModal.vue'
with open(target_path, 'w', encoding='utf-8') as f:
    f.write(modal_code)

print("AtmDetailModal.vue live export fixed successfully!")
