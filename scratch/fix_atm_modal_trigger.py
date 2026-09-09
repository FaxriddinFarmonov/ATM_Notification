import os

# 1. Enhance atmStore.ts fetchAtmDetail to cache under all keys and force fetch support
store_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\stores\atmStore.ts'
with open(store_path, 'r', encoding='utf-8') as f:
    store_code = f.read()

old_fetch = '''  async function fetchAtmDetail(id: number | string, force = false): Promise<AtmDetailResponse | null> {
    if (!force && detailCache.value.has(id)) {
      return detailCache.value.get(id) ?? null;
    }
    isDetailLoading.value = true;
    detailError.value = null;
    try {
      const detail = await atmService.detail(id);
      detailCache.value.set(id, detail);
      return detail;
    } catch (err) {
      detailError.value = extractErrorMessage(err) || "ATM tafsilotlarini yuklab bo'lmadi.";
      return null;
    } finally {
      isDetailLoading.value = false;
    }
  }'''

new_fetch = '''  async function fetchAtmDetail(id: number | string, force = false): Promise<AtmDetailResponse | null> {
    if (!id) return null;
    const idStr = String(id);
    const idNum = Number(id);

    if (!force) {
      const cached =
        detailCache.value.get(id) ||
        detailCache.value.get(idStr) ||
        (!isNaN(idNum) ? detailCache.value.get(idNum) : null);
      if (cached) return cached;
    }

    isDetailLoading.value = true;
    detailError.value = null;
    try {
      const detail = await atmService.detail(id);
      if (detail) {
        detailCache.value.set(id, detail);
        detailCache.value.set(idStr, detail);
        if (!isNaN(idNum)) {
          detailCache.value.set(idNum, detail);
        }
        if (detail.technical?.terminal_id) {
          detailCache.value.set(detail.technical.terminal_id, detail);
        }
      }
      return detail;
    } catch (err) {
      detailError.value = extractErrorMessage(err) || "ATM tafsilotlarini yuklab bo'lmadi.";
      return null;
    } finally {
      isDetailLoading.value = false;
    }
  }'''

store_code = store_code.replace(old_fetch, new_fetch)
with open(store_path, 'w', encoding='utf-8') as f:
    f.write(store_code)
print("atmStore.ts fetchAtmDetail enhanced!")

# 2. Enhance AtmDetailModal.vue computed detail and watcher
modal_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\monitoring\AtmDetailModal.vue'
with open(modal_path, 'r', encoding='utf-8') as f:
    modal_code = f.read()

# Update detail computed
old_detail_comp = '''const detail = computed(() => {
  if (props.atmId == null) return null;
  return atmStore.detailCache.get(props.atmId) ?? null;
});'''

new_detail_comp = '''const detail = computed(() => {
  if (props.atmId == null) return null;
  const idStr = String(props.atmId);
  const idNum = Number(props.atmId);
  return (
    atmStore.detailCache.get(props.atmId) ||
    atmStore.detailCache.get(idStr) ||
    (!isNaN(idNum) ? atmStore.detailCache.get(idNum) : null) ||
    null
  );
});'''

modal_code = modal_code.replace(old_detail_comp, new_detail_comp)

# Update watcher to watch both props.open and props.atmId
old_watch = '''watch(
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
);'''

new_watch = '''watch(
  () => [props.open, props.atmId] as const,
  ([isOpen, currentAtmId]) => {
    if (isOpen && currentAtmId != null) {
      document.body.style.overflow = 'hidden';
      window.addEventListener('keydown', onKeydown);
      atmStore.fetchAtmDetail(currentAtmId);
    } else if (!isOpen) {
      document.body.style.overflow = '';
      window.removeEventListener('keydown', onKeydown);
    }
  },
  { immediate: true }
);'''

modal_code = modal_code.replace(old_watch, new_watch)

with open(modal_path, 'w', encoding='utf-8') as f:
    f.write(modal_code)
print("AtmDetailModal.vue watcher and computed detail enhanced!")

# 3. Enhance BranchAtmsDetailModal.vue openAtmDetail function
branch_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\BranchAtmsDetailModal.vue'
with open(branch_path, 'r', encoding='utf-8') as f:
    branch_code = f.read()

old_branch_handler = '''function openAtmDetail(atm: any) {
  if (!atm) return;
  const targetId = atm.id || atm.atm_id || atm.terminal_id;
  if (!targetId) return;
  selectedAtmId.value = targetId;
  selectedAtmName.value = atm.name || atm.address || `Bankomat (${atm.terminal_id || targetId})`;
  isAtmDetailOpen.value = true;
}'''

new_branch_handler = '''function openAtmDetail(atm: any) {
  if (!atm) return;
  const targetId = atm.id || atm.atm_id || atm.terminal_id;
  if (!targetId) return;
  selectedAtmId.value = targetId;
  selectedAtmName.value = atm.name || atm.address || `Bankomat (${atm.terminal_id || targetId})`;
  isAtmDetailOpen.value = true;
  atmStore.fetchAtmDetail(targetId, true);
}'''

branch_code = branch_code.replace(old_branch_handler, new_branch_handler)

# Make sure useAtmStore is imported in BranchAtmsDetailModal.vue
if 'useAtmStore' not in branch_code:
    branch_code = branch_code.replace(
        "import { atmService } from '@/services/atmService';",
        "import { atmService } from '@/services/atmService';\nimport { useAtmStore } from '@/stores/atmStore';"
    )
    branch_code = branch_code.replace(
        "const { isOpen, selectedRegion, closeModal } = useBranchModal();",
        "const { isOpen, selectedRegion, closeModal } = useBranchModal();\nconst atmStore = useAtmStore();"
    )

with open(branch_path, 'w', encoding='utf-8') as f:
    f.write(branch_code)
print("BranchAtmsDetailModal.vue openAtmDetail handler enhanced!")
