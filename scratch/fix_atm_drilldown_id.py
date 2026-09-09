import os

# 1. Update src/stores/atmStore.ts to accept number | string for ATM detail lookup
store_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\stores\atmStore.ts'
with open(store_path, 'r', encoding='utf-8') as f:
    store_code = f.read()

store_code = store_code.replace(
    'const detailCache = ref<Map<number, AtmDetailResponse>>(new Map());',
    'const detailCache = ref<Map<number | string, AtmDetailResponse>>(new Map());'
)
store_code = store_code.replace(
    'async function fetchAtmDetail(id: number, force = false): Promise<AtmDetailResponse | null> {',
    'async function fetchAtmDetail(id: number | string, force = false): Promise<AtmDetailResponse | null> {'
)

with open(store_path, 'w', encoding='utf-8') as f:
    f.write(store_code)
print("atmStore.ts updated for string | number IDs!")

# 2. Update AtmDetailModal.vue prop types for atmId
modal_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\monitoring\AtmDetailModal.vue'
with open(modal_path, 'r', encoding='utf-8') as f:
    modal_code = f.read()

modal_code = modal_code.replace(
    'atmId: number | null;',
    'atmId: number | string | null;'
)

with open(modal_path, 'w', encoding='utf-8') as f:
    f.write(modal_code)
print("AtmDetailModal.vue prop type updated!")

# 3. Update BranchAtmsDetailModal.vue mapping & click handler
branch_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\BranchAtmsDetailModal.vue'
with open(branch_path, 'r', encoding='utf-8') as f:
    branch_code = f.read()

# Update loadBranchAtms mapping
old_map = '''      atmsList.value = topItems.map(item => ({
        id: item.id,'''

new_map = '''      atmsList.value = topItems.map(item => ({
        id: item.atm_id || item.id || item.terminal_id,'''

branch_code = branch_code.replace(old_map, new_map)

# Update selectedAtmId type & openAtmDetail implementation
old_handler = '''const selectedAtmId = ref<number | null>(null);
const selectedAtmName = ref<string | null>(null);
const isAtmDetailOpen = ref(false);

function openAtmDetail(atm: any) {
  if (!atm || !atm.id) return;
  selectedAtmId.value = atm.id;
  selectedAtmName.value = atm.name || atm.address || "Bankomat";
  isAtmDetailOpen.value = true;
}'''

new_handler = '''const selectedAtmId = ref<number | string | null>(null);
const selectedAtmName = ref<string | null>(null);
const isAtmDetailOpen = ref(false);

function openAtmDetail(atm: any) {
  if (!atm) return;
  const targetId = atm.id || atm.atm_id || atm.terminal_id;
  if (!targetId) return;
  selectedAtmId.value = targetId;
  selectedAtmName.value = atm.name || atm.address || `Bankomat (${atm.terminal_id || targetId})`;
  isAtmDetailOpen.value = true;
}'''

branch_code = branch_code.replace(old_handler, new_handler)

with open(branch_path, 'w', encoding='utf-8') as f:
    f.write(branch_code)

print("BranchAtmsDetailModal.vue drilldown logic fixed!")
