import os

# Update BranchRevenueRanking.vue to add openBranchModal click handlers
path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\dashboard\BranchRevenueRanking.vue'
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

# Add import if not present
if 'useBranchModal' not in code:
    code = code.replace(
        "import Skeleton from '@/components/common/Skeleton.vue';",
        "import Skeleton from '@/components/common/Skeleton.vue';\nimport { useBranchModal } from '@/composables/useBranchModal';"
    )
    code = code.replace(
        "const dashboardStore = useDashboardStore();",
        "const dashboardStore = useDashboardStore();\nconst { openBranchModal } = useBranchModal();"
    )

# Add @click to column item
if '@click="openBranchModal(branch.name)"' not in code:
    code = code.replace(
        "class=\"flex-1 min-w-[58px] sm:min-w-[72px] max-w-[120px] flex flex-col items-center h-full justify-end group cursor-pointer\"",
        "class=\"flex-1 min-w-[58px] sm:min-w-[72px] max-w-[120px] flex flex-col items-center h-full justify-end group cursor-pointer\" @click=\"openBranchModal(branch.name)\""
    )

with open(path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated BranchRevenueRanking.vue successfully!")
