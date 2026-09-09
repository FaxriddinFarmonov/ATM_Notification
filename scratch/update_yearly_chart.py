import os

vue_code = '''<template>
  <div class="w-full">
    <!-- PDF Hidden Export Template (Formal Bank Document Layout) -->
    <div
      id="pdf-report-template"
      class="fixed left-[-9999px] top-[-9999px] w-[1120px] bg-slate-950 text-white p-8 space-y-6 font-sans border border-slate-800"
    >
      <!-- Formal Document Header -->
      <div class="flex items-center justify-between border-b border-slate-800 pb-5">
        <div class="flex items-center gap-4">
          <div class="p-3 bg-blue-600/20 rounded-2xl border border-blue-500/30">
            <Scale class="w-8 h-8 text-blue-400" />
          </div>
          <div>
            <h1 class="text-2xl font-black text-white tracking-tight uppercase">TURONBANK ATB</h1>
            <p class="text-xs text-sky-400 font-bold tracking-wide mt-0.5">
              ATM VA TERMINALLAR MOLIYAVIY TAQQOSLASH VA ANALITIKA HISOBOTI
            </p>
          </div>
        </div>
        <div class="text-right text-xs text-slate-300 space-y-1">
          <p><span class="text-slate-400">Taqqoslash Yillari:</span> <strong class="text-sky-300 font-extrabold">{{ yearA }}-yil</strong> vs <strong class="text-emerald-300 font-extrabold">{{ yearB }}-yil</strong></p>
          <p><span class="text-slate-400">Tanlangan Ko'rsatkich:</span> <strong class="text-purple-300 font-extrabold">{{ getMetricLabel(selectedMetric) }}</strong></p>
          <p><span class="text-slate-400">Hujjat Sanasi:</span> <strong class="text-white font-bold">{{ documentDateStr }}</strong></p>
        </div>
      </div>

      <!-- Executive KPI Summary Cards Grid -->
      <div class="grid grid-cols-4 gap-4">
        <div class="p-4 rounded-xl bg-slate-900 border border-blue-500/30">
          <div class="text-[11px] font-bold text-slate-400 mb-1">{{ yearA }}-yil Jami ({{ getMetricLabel(selectedMetric) }}):</div>
          <div class="text-lg font-black text-sky-300">{{ formatUzSum(getMetricTotal(selectedMetric, 'a')) }}</div>
        </div>
        <div class="p-4 rounded-xl bg-slate-900 border border-emerald-500/30">
          <div class="text-[11px] font-bold text-slate-400 mb-1">{{ yearB }}-yil Jami ({{ getMetricLabel(selectedMetric) }}):</div>
          <div class="text-lg font-black text-emerald-300">{{ formatUzSum(getMetricTotal(selectedMetric, 'b')) }}</div>
        </div>
        <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
          <div class="text-[11px] font-bold text-slate-400 mb-1">Farq (So'mda {{ yearB }} - {{ yearA }}):</div>
          <div :class="['text-lg font-black', getDiffVal(selectedMetric) >= 0 ? 'text-emerald-400' : 'text-rose-400']">
            {{ (getDiffVal(selectedMetric) >= 0 ? '+' : '') + formatUzSum(getDiffVal(selectedMetric)) }}
          </div>
        </div>
        <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
          <div class="text-[11px] font-bold text-slate-400 mb-1">O'sish Dinamikasi (%):</div>
          <div :class="['text-lg font-black', getGrowthPct(selectedMetric) >= 0 ? 'text-emerald-400' : 'text-rose-400']">
            {{ (getGrowthPct(selectedMetric) >= 0 ? '+' : '') + getGrowthPct(selectedMetric).toFixed(2) }}%
          </div>
        </div>
      </div>

      <!-- Chart Snapshot Box in PDF -->
      <div class="p-5 bg-slate-900/90 rounded-2xl border border-slate-800 space-y-3">
        <div class="flex items-center justify-between text-xs font-bold text-slate-200">
          <span>Oylar Kesimida Dinamika Graph ({{ getMetricLabel(selectedMetric) }})</span>
          <div class="flex items-center gap-4 text-xs font-bold">
            <span class="text-sky-400">● {{ yearA }}-yil</span>
            <span class="text-emerald-400">● {{ yearB }}-yil</span>
          </div>
        </div>
        <div class="relative h-64 w-full flex items-end pt-4 pb-2 border-b border-slate-800">
          <div v-for="m in comparisonData?.months" :key="m.month" class="flex-1 flex flex-col items-center justify-end h-full relative">
            <div class="flex items-end justify-center gap-1.5 w-full h-full">
              <div class="w-3 bg-sky-500 rounded-t-sm" :style="{ height: getBarHeight(getValByMetric(m, selectedMetric, 'a')) }"></div>
              <div class="w-3 bg-emerald-400 rounded-t-sm" :style="{ height: getBarHeight(getValByMetric(m, selectedMetric, 'b')) }"></div>
            </div>
            <span class="text-[10px] font-bold text-slate-400 mt-1.5">{{ m.name.substring(0, 3) }}</span>
          </div>
        </div>
      </div>

      <!-- Detailed Monthly Analytics Table in PDF -->
      <div class="space-y-3">
        <h3 class="text-sm font-extrabold text-white flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-purple-500"></span>
          Oylar Kesimida Batafsil Taqqoslash va Analitika Jadvali
        </h3>
        <table class="w-full text-xs border-collapse text-left bg-slate-900 rounded-xl overflow-hidden border border-slate-800">
          <thead>
            <tr class="bg-slate-800/80 text-slate-300 font-bold border-b border-slate-700">
              <th class="p-2.5 text-center w-12">№</th>
              <th class="p-2.5">Oy Nomi</th>
              <th class="p-2.5 text-right">{{ yearA }}-yil (So'm)</th>
              <th class="p-2.5 text-right">{{ yearB }}-yil (So'm)</th>
              <th class="p-2.5 text-right">Farq (So'm)</th>
              <th class="p-2.5 text-center">O'sish (%)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800/60 text-slate-200">
            <tr v-for="(m, idx) in comparisonData?.months" :key="m.month" class="hover:bg-slate-800/30">
              <td class="p-2.5 text-center text-slate-400 font-bold">{{ idx + 1 }}</td>
              <td class="p-2.5 font-bold text-white">{{ m.name }}</td>
              <td class="p-2.5 text-right font-semibold text-sky-400">{{ formatUzSum(getValByMetric(m, selectedMetric, 'a')) }}</td>
              <td class="p-2.5 text-right font-semibold text-emerald-400">{{ formatUzSum(getValByMetric(m, selectedMetric, 'b')) }}</td>
              <td class="p-2.5 text-right font-bold" :class="getValDiff(m) >= 0 ? 'text-emerald-400' : 'text-rose-400'">
                {{ (getValDiff(m) >= 0 ? '+' : '') + formatUzSum(getValDiff(m)) }}
              </td>
              <td class="p-2.5 text-center font-bold" :class="getValGrowth(m) >= 0 ? 'text-emerald-400' : 'text-rose-400'">
                {{ (getValGrowth(m) >= 0 ? '+' : '') + getValGrowth(m).toFixed(1) }}%
              </td>
            </tr>
          </tbody>
          <tfoot>
            <tr class="bg-slate-800/90 font-black text-white border-t-2 border-slate-700">
              <td colspan="2" class="p-2.5 text-right uppercase">Jami Kassa / Ko'rsatkich:</td>
              <td class="p-2.5 text-right text-sky-300">{{ formatUzSum(getMetricTotal(selectedMetric, 'a')) }}</td>
              <td class="p-2.5 text-right text-emerald-300">{{ formatUzSum(getMetricTotal(selectedMetric, 'b')) }}</td>
              <td class="p-2.5 text-right" :class="getDiffVal(selectedMetric) >= 0 ? 'text-emerald-400' : 'text-rose-400'">
                {{ (getDiffVal(selectedMetric) >= 0 ? '+' : '') + formatUzSum(getDiffVal(selectedMetric)) }}
              </td>
              <td class="p-2.5 text-center" :class="getGrowthPct(selectedMetric) >= 0 ? 'text-emerald-400' : 'text-rose-400'">
                {{ (getGrowthPct(selectedMetric) >= 0 ? '+' : '') + getGrowthPct(selectedMetric).toFixed(2) }}%
              </td>
            </tr>
          </tfoot>
        </table>
      </div>

      <!-- Formal Footer -->
      <div class="pt-4 border-t border-slate-800 text-[10px] text-slate-500 flex justify-between">
        <span>Turonbank ATB Avtomatlashtirilgan Analitika Portali</span>
        <span>Hujjat maxfiylik darajasi: Ichki foydalanish uchun</span>
      </div>
    </div>

    <!-- On-Screen Main Interactive Component Container -->
    <div id="yearly-comparison-report" class="bg-slate-900/90 rounded-3xl p-6 sm:p-7 border border-slate-700/60 shadow-2xl text-white space-y-6">
      <!-- Portal Header Section -->
      <div class="flex flex-col xl:flex-row xl:items-center justify-between gap-5 border-b border-slate-800 pb-5">
        <div class="flex items-center gap-4">
          <div class="p-3.5 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-600 text-white shadow-lg shadow-blue-500/20">
            <Scale class="w-7 h-7" />
          </div>
          <div>
            <div class="flex items-center gap-2 text-xs font-bold text-sky-400 tracking-wider uppercase">
              <span>YILLIK DINAMIKA & TAQQOSLASH</span>
              <span>•</span>
              <span>Oylar Kesimida Analitika</span>
            </div>
            <h2 class="text-2xl sm:text-3xl font-black text-white tracking-tight mt-0.5">
              Yillar Bo'yicha <span class="bg-gradient-to-r from-sky-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">Moliyaviy Taqqoslash Portali</span>
            </h2>
            <p class="text-xs text-slate-400 mt-1">
              2024, 2025 va 2026-yillar davomidagi daromadlar, haqiqiy rasxodlar hamda naqd pul aylanmasini taqqoslash
            </p>
          </div>
        </div>

        <!-- Controls Toolbar -->
        <div class="flex flex-wrap items-center gap-3">
          <!-- Years Selector Pair -->
          <div class="flex items-center gap-2 px-4 py-2.5 rounded-2xl bg-slate-950/90 border border-slate-700/80 shadow-inner text-xs font-bold">
            <select v-model="yearA" class="bg-transparent font-black text-sky-400 outline-none cursor-pointer text-sm">
              <option :value="2025" class="bg-slate-900 text-white">1-yil: 2025-yil</option>
              <option :value="2024" class="bg-slate-900 text-white">1-yil: 2024-yil</option>
              <option :value="2026" class="bg-slate-900 text-white">1-yil: 2026-yil</option>
            </select>

            <span class="text-slate-500 font-extrabold uppercase px-1">VS</span>

            <select v-model="yearB" class="bg-transparent font-black text-emerald-400 outline-none cursor-pointer text-sm">
              <option :value="2026" class="bg-slate-900 text-white">2-yil: 2026-yil (6 oy)</option>
              <option :value="2025" class="bg-slate-900 text-white">2-yil: 2025-yil</option>
              <option :value="2024" class="bg-slate-900 text-white">2-yil: 2024-yil</option>
            </select>
          </div>

          <!-- Metric Selector -->
          <select v-model="selectedMetric" class="bg-slate-950/90 border border-slate-700/80 px-4 py-2.5 rounded-2xl text-xs font-extrabold text-white outline-none cursor-pointer focus:border-purple-500 shadow-inner">
            <option value="income" class="bg-slate-900">Jami Daromad</option>
            <option value="expense" class="bg-slate-900">Haqiqiy Rasxod</option>
            <option value="net_profit" class="bg-slate-900">Sof Foyda</option>
            <option value="cash_withdrawal" class="bg-slate-900">Naqd Pul Yechish</option>
          </select>

          <!-- Chart Type Toggle (Bar vs Line) -->
          <div class="inline-flex p-1.5 rounded-2xl bg-slate-950/90 border border-slate-700/80 text-xs">
            <button
              @click="chartType = 'bar'"
              :class="['px-3.5 py-1.5 rounded-xl font-bold transition-all', chartType === 'bar' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-400 hover:text-white']"
            >
              Bar
            </button>
            <button
              @click="chartType = 'line'"
              :class="['px-3.5 py-1.5 rounded-xl font-bold transition-all', chartType === 'line' ? 'bg-purple-600 text-white shadow-md' : 'text-slate-400 hover:text-white']"
            >
              Line
            </button>
          </div>

          <!-- Download PDF Button -->
          <button
            @click="exportPdf"
            :disabled="isExporting"
            class="flex items-center gap-2 px-5 py-2.5 rounded-2xl bg-gradient-to-r from-red-600 via-rose-600 to-pink-600 hover:from-red-500 hover:to-pink-500 text-white font-extrabold text-xs shadow-lg shadow-red-500/25 border border-red-400/40 transition-all active:scale-95 disabled:opacity-50"
          >
            <Download class="w-4 h-4" />
            <span>{{ isExporting ? 'PDF Yasalmoqda...' : 'Download PDF' }}</span>
          </button>
        </div>
      </div>

      <!-- Loading / Error States -->
      <div v-if="isLoading" class="py-16 text-center text-slate-400 flex items-center justify-center gap-3">
        <div class="w-6 h-6 border-3 border-purple-400 border-t-transparent rounded-full animate-spin"></div>
        <span class="font-bold text-sm">Taqqoslash ma'lumotlari yuklanmoqda...</span>
      </div>

      <div v-else-if="error" class="p-5 rounded-2xl bg-red-950/60 border border-red-500/40 text-red-200 text-xs flex items-center justify-between">
        <span>{{ error }}</span>
        <button @click="fetchComparison" class="px-4 py-2 bg-red-800 hover:bg-red-700 rounded-xl text-white font-bold transition-colors">
          Qayta urinish
        </button>
      </div>

      <!-- Main Visual & Summary Content -->
      <div v-else-if="comparisonData" class="space-y-6">
        <!-- 4 Key Comparison Summary Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <!-- Year A Total -->
          <div class="p-5 rounded-2xl bg-slate-950/80 border border-blue-500/30 shadow-md">
            <div class="text-xs font-bold text-slate-400 mb-1 flex items-center justify-between">
              <span>{{ yearA }}-yil Jami ({{ getMetricLabel(selectedMetric) }}):</span>
              <span class="w-2.5 h-2.5 rounded-full bg-sky-400 shadow-sm shadow-sky-400"></span>
            </div>
            <div class="text-xl sm:text-2xl font-black text-sky-300 mt-1">
              {{ formatUzSum(getMetricTotal(selectedMetric, 'a')) }}
            </div>
          </div>

          <!-- Year B Total -->
          <div class="p-5 rounded-2xl bg-slate-950/80 border border-emerald-500/30 shadow-md">
            <div class="text-xs font-bold text-slate-400 mb-1 flex items-center justify-between">
              <span>{{ yearB }}-yil Jami ({{ getMetricLabel(selectedMetric) }}):</span>
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400"></span>
            </div>
            <div class="text-xl sm:text-2xl font-black text-emerald-400 mt-1">
              {{ formatUzSum(getMetricTotal(selectedMetric, 'b')) }}
            </div>
          </div>

          <!-- Absolute Difference -->
          <div class="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 shadow-md">
            <div class="text-xs font-bold text-slate-400 mb-1">
              Farq ( So'mda {{ yearB }} - {{ yearA }} ):
            </div>
            <div :class="['text-xl sm:text-2xl font-black mt-1', getDiffVal(selectedMetric) >= 0 ? 'text-emerald-400' : 'text-rose-400']">
              {{ (getDiffVal(selectedMetric) >= 0 ? '+' : '') + formatUzSum(getDiffVal(selectedMetric)) }}
            </div>
          </div>

          <!-- Growth Percentage -->
          <div class="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 shadow-md">
            <div class="text-xs font-bold text-slate-400 mb-1">
              O'sish Dinamikasi (%):
            </div>
            <div :class="['text-xl sm:text-2xl font-black mt-1 flex items-center gap-1.5', getGrowthPct(selectedMetric) >= 0 ? 'text-emerald-400' : 'text-rose-400']">
              <TrendingUp v-if="getGrowthPct(selectedMetric) >= 0" class="w-6 h-6" />
              <TrendingDown v-else class="w-6 h-6" />
              <span>{{ (getGrowthPct(selectedMetric) >= 0 ? '+' : '') + getGrowthPct(selectedMetric).toFixed(2) }}%</span>
            </div>
          </div>
        </div>

        <!-- Custom Visualizer Canvas Container (Enlarged Height) -->
        <div class="p-6 rounded-2xl bg-slate-950 border border-slate-800/90 shadow-inner space-y-5">
          <div class="flex items-center justify-between text-xs text-slate-300 flex-wrap gap-2">
            <div class="font-bold text-white text-sm flex items-center gap-2">
              <span class="w-3 h-3 rounded-full bg-purple-500"></span>
              Oylar Kesimida Taqqoslash: {{ getMetricLabel(selectedMetric) }} ({{ yearA }} vs {{ yearB }})
            </div>
            <div class="flex items-center gap-5 text-xs font-bold">
              <span class="flex items-center gap-2 text-sky-400">
                <span class="w-3.5 h-3.5 rounded-sm bg-sky-500"></span> {{ yearA }}-yil
              </span>
              <span class="flex items-center gap-2 text-emerald-400">
                <span class="w-3.5 h-3.5 rounded-sm bg-emerald-400"></span> {{ yearB }}-yil
              </span>
            </div>
          </div>

          <!-- Graphic Chart Container (Height h-80 = 320px) -->
          <div class="relative grid grid-cols-12 gap-2 sm:gap-4 items-end h-80 pt-8 pb-4 border-b border-slate-800 px-3">
            
            <!-- SVG Vector Overlay for Line Chart mode -->
            <svg
              v-if="chartType === 'line'"
              class="absolute inset-0 w-full h-full pointer-events-none z-10 overflow-visible"
              viewBox="0 0 1200 320"
              preserveAspectRatio="none"
            >
              <defs>
                <filter id="glow-line-sky" x="-20%" y="-20%" width="140%" height="140%">
                  <feGaussianBlur stdDeviation="3" result="blur" />
                  <feMerge>
                    <feMergeNode in="blur" />
                    <feMergeNode in="SourceGraphic" />
                  </feMerge>
                </filter>
                <filter id="glow-line-emerald" x="-20%" y="-20%" width="140%" height="140%">
                  <feGaussianBlur stdDeviation="3" result="blur" />
                  <feMerge>
                    <feMergeNode in="blur" />
                    <feMergeNode in="SourceGraphic" />
                  </feMerge>
                </filter>
              </defs>

              <!-- Year A Line (Sky Blue) -->
              <path
                :d="svgLinePathA"
                fill="none"
                stroke="#38bdf8"
                stroke-width="4"
                stroke-linecap="round"
                stroke-linejoin="round"
                filter="url(#glow-line-sky)"
              />

              <!-- Year B Line (Emerald Green) -->
              <path
                :d="svgLinePathB"
                fill="none"
                stroke="#34d399"
                stroke-width="4"
                stroke-linecap="round"
                stroke-linejoin="round"
                filter="url(#glow-line-emerald)"
              />
            </svg>

            <!-- 12 Month Column Items -->
            <div
              v-for="m in comparisonData.months"
              :key="m.month"
              class="flex flex-col items-center h-full justify-end group relative z-20"
            >
              <!-- Clear Large Hover Tooltip -->
              <div class="absolute -top-20 left-1/2 -translate-x-1/2 hidden group-hover:flex flex-col items-center bg-slate-900 border border-slate-700/90 px-3.5 py-2 rounded-xl text-xs whitespace-nowrap z-40 shadow-2xl pointer-events-none">
                <span class="font-extrabold text-white mb-1 text-sm border-b border-slate-700 pb-0.5 w-full text-center">{{ m.name }}</span>
                <span class="text-sky-400 font-bold">{{ yearA }}: {{ formatUzSum(getValByMetric(m, selectedMetric, 'a')) }}</span>
                <span class="text-emerald-400 font-bold">{{ yearB }}: {{ formatUzSum(getValByMetric(m, selectedMetric, 'b')) }}</span>
                <span :class="['text-[11px] font-extrabold mt-0.5', getValDiff(m) >= 0 ? 'text-emerald-400' : 'text-rose-400']">
                  Farq: {{ (getValDiff(m) >= 0 ? '+' : '') + formatUzSum(getValDiff(m)) }}
                </span>
              </div>

              <!-- Bar Comparison Pair -->
              <div v-if="chartType === 'bar'" class="flex items-end justify-center gap-1.5 w-full h-full">
                <!-- Bar A -->
                <div
                  class="w-1/2 max-w-[20px] bg-gradient-to-t from-blue-700 via-sky-500 to-sky-300 rounded-t-md transition-all duration-500 group-hover:brightness-125 shadow-md shadow-sky-500/20"
                  :style="{ height: getBarHeight(getValByMetric(m, selectedMetric, 'a')) }"
                ></div>
                <!-- Bar B -->
                <div
                  class="w-1/2 max-w-[20px] bg-gradient-to-t from-emerald-700 via-teal-400 to-emerald-300 rounded-t-md transition-all duration-500 group-hover:brightness-125 shadow-md shadow-emerald-500/20"
                  :style="{ height: getBarHeight(getValByMetric(m, selectedMetric, 'b')) }"
                ></div>
              </div>

              <!-- Line Chart Glowing Points -->
              <div v-else class="flex flex-col justify-end items-center w-full h-full relative">
                <!-- Dot A -->
                <div
                  class="absolute w-4 h-4 rounded-full bg-sky-400 border-2 border-slate-900 shadow-lg shadow-sky-500 z-30 transition-all duration-500 group-hover:scale-125"
                  :style="{ bottom: getBarHeight(getValByMetric(m, selectedMetric, 'a')) }"
                ></div>
                <!-- Dot B -->
                <div
                  class="absolute w-4 h-4 rounded-full bg-emerald-400 border-2 border-slate-900 shadow-lg shadow-emerald-500 z-30 transition-all duration-500 group-hover:scale-125"
                  :style="{ bottom: getBarHeight(getValByMetric(m, selectedMetric, 'b')) }"
                ></div>
              </div>

              <!-- Month Label -->
              <span class="text-xs font-bold text-slate-300 mt-3 truncate w-full text-center group-hover:text-purple-400 transition-colors">
                {{ m.name.substring(0, 3) }}
              </span>
            </div>
          </div>
        </div>

        <!-- On-Screen Detailed Monthly Financial Breakdown Table -->
        <div class="bg-slate-950/80 rounded-2xl p-5 border border-slate-800 space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-extrabold text-white flex items-center gap-2">
              <span class="w-3 h-3 rounded-full bg-emerald-400"></span>
              Oylar Kesimida Batafsil Taqqoslash va Analitika Jadvali
            </h3>
            <span class="text-xs text-slate-400 font-semibold">Toliq oylik ko'rsatkichlar</span>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-xs text-left">
              <thead class="bg-slate-900 text-slate-400 font-extrabold border-b border-slate-800 uppercase">
                <tr>
                  <th class="p-3 text-center w-12">№</th>
                  <th class="p-3">Oy Nomi</th>
                  <th class="p-3 text-right">{{ yearA }}-yil Ko'rsatkich</th>
                  <th class="p-3 text-right">{{ yearB }}-yil Ko'rsatkich</th>
                  <th class="p-3 text-right">Farq (So'm)</th>
                  <th class="p-3 text-center">O'sish Dinamikasi (%)</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-800/80 font-medium">
                <tr
                  v-for="(m, idx) in comparisonData.months"
                  :key="m.month"
                  class="hover:bg-slate-900/60 transition-colors"
                >
                  <td class="p-3 text-center font-bold text-slate-500">{{ idx + 1 }}</td>
                  <td class="p-3 font-extrabold text-white text-sm">{{ m.name }}</td>
                  <td class="p-3 text-right font-bold text-sky-400 text-sm">
                    {{ formatUzSum(getValByMetric(m, selectedMetric, 'a')) }}
                  </td>
                  <td class="p-3 text-right font-bold text-emerald-400 text-sm">
                    {{ formatUzSum(getValByMetric(m, selectedMetric, 'b')) }}
                  </td>
                  <td class="p-3 text-right font-black text-sm" :class="getValDiff(m) >= 0 ? 'text-emerald-400' : 'text-rose-400'">
                    {{ (getValDiff(m) >= 0 ? '+' : '') + formatUzSum(getValDiff(m)) }}
                  </td>
                  <td class="p-3 text-center font-black text-sm" :class="getValGrowth(m) >= 0 ? 'text-emerald-400' : 'text-rose-400'">
                    {{ (getValGrowth(m) >= 0 ? '+' : '') + getValGrowth(m).toFixed(1) }}%
                  </td>
                </tr>
              </tbody>
              <tfoot>
                <tr class="bg-slate-900 font-black text-white border-t-2 border-slate-700">
                  <td colspan="2" class="p-3.5 text-right uppercase text-sm">Jami ({{ getMetricLabel(selectedMetric) }}):</td>
                  <td class="p-3.5 text-right text-sky-300 text-base">{{ formatUzSum(getMetricTotal(selectedMetric, 'a')) }}</td>
                  <td class="p-3.5 text-right text-emerald-300 text-base">{{ formatUzSum(getMetricTotal(selectedMetric, 'b')) }}</td>
                  <td class="p-3.5 text-right text-base" :class="getDiffVal(selectedMetric) >= 0 ? 'text-emerald-400' : 'text-rose-400'">
                    {{ (getDiffVal(selectedMetric) >= 0 ? '+' : '') + formatUzSum(getDiffVal(selectedMetric)) }}
                  </td>
                  <td class="p-3.5 text-center text-base" :class="getGrowthPct(selectedMetric) >= 0 ? 'text-emerald-400' : 'text-rose-400'">
                    {{ (getGrowthPct(selectedMetric) >= 0 ? '+' : '') + getGrowthPct(selectedMetric).toFixed(2) }}%
                  </td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { analyticsService, type YearlyComparisonResponse } from '@/services/analyticsService';
import { Scale, TrendingUp, TrendingDown, Download } from 'lucide-vue-next';
import html2canvas from 'html2canvas';
import { jsPDF } from 'jspdf';

const yearA = ref<number>(2025);
const yearB = ref<number>(2026);
const selectedMetric = ref<'income' | 'expense' | 'net_profit' | 'cash_withdrawal'>('income');
const chartType = ref<'bar' | 'line'>('bar');
const isLoading = ref<boolean>(true);
const isExporting = ref<boolean>(false);
const error = ref<string | null>(null);
const comparisonData = ref<YearlyComparisonResponse | null>(null);

const documentDateStr = computed(() => {
  return new Date().toLocaleDateString('uz-UZ', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
});

async function fetchComparison() {
  isLoading.value = true;
  error.value = null;
  try {
    const data = await analyticsService.getYearlyComparison(yearA.value, yearB.value);
    comparisonData.value = data;
  } catch (err: any) {
    console.error("Comparison API error:", err);
    error.value = err?.message || "Taqqoslash ma'lumotlarini yuklashda xatolik yuz berdi";
  } finally {
    isLoading.value = false;
  }
}

watch([yearA, yearB], () => {
  fetchComparison();
});

onMounted(() => {
  fetchComparison();
});

function getValByMetric(item: any, metric: string, suffix: 'a' | 'b'): number {
  if (!item) return 0;
  const key = `${metric}_${suffix}`;
  return item[key] || 0;
}

function getMetricLabel(metric: string): string {
  switch (metric) {
    case 'income': return "Jami Daromad";
    case 'expense': return "Haqiqiy Rasxod";
    case 'net_profit': return "Sof Foyda";
    case 'cash_withdrawal': return "Naqd Pul Yechish";
    default: return metric;
  }
}

function getMetricTotal(metric: string, suffix: 'a' | 'b'): number {
  if (!comparisonData.value?.summary) return 0;
  const s = comparisonData.value.summary as any;
  const key = `${metric}_${suffix}`;
  return s[key] || 0;
}

function getDiffVal(metric: string): number {
  if (!comparisonData.value?.summary) return 0;
  const s = comparisonData.value.summary as any;
  const key = `${metric}_diff`;
  return s[key] || 0;
}

function getGrowthPct(metric: string): number {
  if (!comparisonData.value?.summary) return 0;
  const s = comparisonData.value.summary as any;
  const key = `${metric}_growth_pct`;
  return s[key] || 0;
}

function getValDiff(m: any): number {
  const valA = getValByMetric(m, selectedMetric.value, 'a');
  const valB = getValByMetric(m, selectedMetric.value, 'b');
  return valB - valA;
}

function getValGrowth(m: any): number {
  const valA = getValByMetric(m, selectedMetric.value, 'a');
  const valB = getValByMetric(m, selectedMetric.value, 'b');
  if (!valA || valA === 0) return valB > 0 ? 100 : 0;
  return ((valB - valA) / Math.abs(valA)) * 100;
}

const maxMetricVal = computed(() => {
  if (!comparisonData.value?.months) return 1;
  let max = 0;
  comparisonData.value.months.forEach(m => {
    const valA = Math.abs(getValByMetric(m, selectedMetric.value, 'a'));
    const valB = Math.abs(getValByMetric(m, selectedMetric.value, 'b'));
    if (valA > max) max = valA;
    if (valB > max) max = valB;
  });
  return max > 0 ? max : 1;
});

function getBarHeightPctNum(val: number): number {
  const abs = Math.abs(val);
  return Math.max(5, Math.min(88, Math.round((abs / maxMetricVal.value) * 100)));
}

function getBarHeight(val: number): string {
  return `${getBarHeightPctNum(val)}%`;
}

// SVG Line Calculation for 1200x320 viewBox
const svgLinePathA = computed(() => {
  if (!comparisonData.value?.months?.length) return '';
  const months = comparisonData.value.months;
  const points = months.map((m, i) => {
    const x = (i + 0.5) * (1200 / 12);
    const pct = getBarHeightPctNum(getValByMetric(m, selectedMetric.value, 'a'));
    const y = 320 - 45 - (pct / 100) * 230;
    return { x, y };
  });
  return buildSmoothPath(points);
});

const svgLinePathB = computed(() => {
  if (!comparisonData.value?.months?.length) return '';
  const months = comparisonData.value.months;
  const points = months.map((m, i) => {
    const x = (i + 0.5) * (1200 / 12);
    const pct = getBarHeightPctNum(getValByMetric(m, selectedMetric.value, 'b'));
    const y = 320 - 45 - (pct / 100) * 230;
    return { x, y };
  });
  return buildSmoothPath(points);
});

function buildSmoothPath(points: { x: number; y: number }[]): string {
  if (!points || points.length === 0) return '';
  if (points.length === 1) return `M ${points[0].x} ${points[0].y}`;
  let path = `M ${points[0].x} ${points[0].y}`;
  for (let i = 0; i < points.length - 1; i++) {
    const curr = points[i];
    const next = points[i + 1];
    const cp1x = curr.x + (next.x - curr.x) / 2;
    const cp1y = curr.y;
    const cp2x = curr.x + (next.x - curr.x) / 2;
    const cp2y = next.y;
    path += ` C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${next.x} ${next.y}`;
  }
  return path;
}

function formatUzSum(val: number): string {
  if (val === undefined || val === null || isNaN(val)) return "0 so'm";
  const abs = Math.abs(val);
  if (abs >= 1_000_000_000_000) return (val / 1_000_000_000_000).toFixed(2) + " Trln so'm";
  if (abs >= 1_000_000_000) return (val / 1_000_000_000).toFixed(2) + " Mlrd so'm";
  if (abs >= 1_000_000) return (val / 1_000_000).toFixed(2) + " Mln so'm";
  if (abs >= 1_000) return (val / 1_000).toFixed(1) + " MING so'm";
  return val.toLocaleString('uz-UZ') + " so'm";
}

async function exportPdf() {
  if (isExporting.value) return;
  isExporting.value = true;
  try {
    const element = document.getElementById('pdf-report-template');
    if (!element) return;

    // Bring into temporary view for snapshot capture
    element.style.left = '0px';
    element.style.top = '0px';
    element.style.zIndex = '99999';

    const canvas = await html2canvas(element, {
      scale: 2,
      useCORS: true,
      backgroundColor: '#020617',
      logging: false
    });

    element.style.left = '-9999px';
    element.style.top = '-9999px';
    element.style.zIndex = '-1';

    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4'
    });

    const pdfWidth = 210;
    const pdfHeight = 297;
    const imgWidth = 194;
    const imgHeight = (canvas.height * imgWidth) / canvas.width;

    pdf.setFillColor(2, 6, 23);
    pdf.rect(0, 0, pdfWidth, pdfHeight, 'F');
    pdf.addImage(imgData, 'PNG', 8, 8, imgWidth, Math.min(imgHeight, pdfHeight - 16));

    pdf.save(`Turonbank_ATM_Taqqoslash_${yearA.value}_vs_${yearB.value}.pdf`);
  } catch (err) {
    console.error("PDF export error:", err);
  } finally {
    isExporting.value = false;
  }
}
</script>
'''

target = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\dashboard\YearlyComparisonChart.vue'
with open(target, 'w', encoding='utf-8') as f:
    f.write(vue_code)
print("Updated successfully!")
