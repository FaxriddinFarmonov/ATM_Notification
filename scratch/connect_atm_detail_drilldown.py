import os

# 1. Update AtmDetailModal.vue z-index to z-[110] for modal stacking
atm_modal_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\monitoring\AtmDetailModal.vue'
with open(atm_modal_path, 'r', encoding='utf-8') as f:
    modal_code = f.read()

modal_code = modal_code.replace('z-[100]', 'z-[110]')
with open(atm_modal_path, 'w', encoding='utf-8') as f:
    f.write(modal_code)

print("AtmDetailModal.vue z-index set to z-[110]!")

# 2. Update BranchAtmsDetailModal.vue to enable row clicks and open AtmDetailModal
branch_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\BranchAtmsDetailModal.vue'
with open(branch_path, 'r', encoding='utf-8') as f:
    branch_code = f.read()

# Add clickable table row styles and click handler
old_tr = '''                  <tr
                    v-for="(atm, idx) in filteredAtms"
                    :key="atm.id || atm.terminal_id"
                    class="hover:bg-slate-900/60 transition-colors"
                  >'''

new_tr = '''                  <tr
                    v-for="(atm, idx) in filteredAtms"
                    :key="atm.id || atm.terminal_id"
                    @click="openAtmDetail(atm)"
                    class="hover:bg-slate-800/80 cursor-pointer transition-colors group"
                  >'''

branch_code = branch_code.replace(old_tr, new_tr)

# Highlight name on hover
old_name = '''                    <td class="p-3">
                      <div class="font-bold text-white text-sm">{{ atm.name || 'Bankomat' }}</div>'''

new_name = '''                    <td class="p-3">
                      <div class="font-bold text-white text-sm group-hover:text-sky-400 transition-colors flex items-center gap-1.5">
                        <span>{{ atm.name || 'Bankomat' }}</span>
                        <ExternalLink class="w-3.5 h-3.5 opacity-0 group-hover:opacity-100 text-sky-400 transition-opacity shrink-0" />
                      </div>'''

branch_code = branch_code.replace(old_name, new_name)

# Include AtmDetailModal component at bottom of template before </Teleport>
if '<AtmDetailModal' not in branch_code:
    branch_code = branch_code.replace(
        '</Teleport>',
        '    <AtmDetailModal\n      v-model:open="isAtmDetailOpen"\n      :atm-id="selectedAtmId"\n      :fallback-name="selectedAtmName"\n    />\n  </Teleport>'
    )

# Add imports and script logic
if 'AtmDetailModal' not in branch_code:
    branch_code = branch_code.replace(
        "import { ref, computed, watch } from 'vue';",
        "import { ref, computed, watch } from 'vue';\nimport AtmDetailModal from '@/components/monitoring/AtmDetailModal.vue';\nimport { ExternalLink } from 'lucide-vue-next';"
    )

# Add reactive state for AtmDetailModal
state_code = '''const { isOpen, selectedRegion, closeModal } = useBranchModal();

const selectedAtmId = ref<number | null>(null);
const selectedAtmName = ref<string | null>(null);
const isAtmDetailOpen = ref(false);

function openAtmDetail(atm: any) {
  if (!atm || !atm.id) return;
  selectedAtmId.value = atm.id;
  selectedAtmName.value = atm.name || atm.address || "Bankomat";
  isAtmDetailOpen.value = true;
}'''

branch_code = branch_code.replace('const { isOpen, selectedRegion, closeModal } = useBranchModal();', state_code)

with open(branch_path, 'w', encoding='utf-8') as f:
    f.write(branch_code)

print("BranchAtmsDetailModal.vue drilldown connected successfully!")
