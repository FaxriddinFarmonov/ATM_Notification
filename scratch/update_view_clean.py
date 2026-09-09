path_view = r"C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\views\AiAnalyticsView.vue"

new_view = """<template>
  <div class="py-2">
    <!-- Main AI Bankomat Hub Showcase -->
    <AiBankomatPortalHub @select-tab="store.setTab($event)" />

    <!-- Modals for ATM & Region AI details -->
    <SingleAtmAiModal />
    <RegionAiModal />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useAnalyticsStore } from '@/stores/analyticsStore';
import AiBankomatPortalHub from '@/components/analytics/AiBankomatPortalHub.vue';
import SingleAtmAiModal from '@/components/analytics/SingleAtmAiModal.vue';
import RegionAiModal from '@/components/analytics/RegionAiModal.vue';

const store = useAnalyticsStore();

onMounted(() => {
  store.fetchCurrentTabData();
});
</script>
"""

with open(path_view, 'w', encoding='utf-8') as f:
    f.write(new_view)

print("Updated AiAnalyticsView.vue to clean main page with only Hub and Modals")
