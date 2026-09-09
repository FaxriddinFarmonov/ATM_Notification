path_hub = r"C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\AiBankomatPortalHub.vue"
with open(path_hub, 'r', encoding='utf-8') as f:
    hub_code = f.read()

path_view = r"C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\views\AiAnalyticsView.vue"
with open(path_view, 'r', encoding='utf-8') as f:
    view_code = f.read()

print("--- HUB BOTTOM PART ---")
print(hub_code[hub_code.find("Bottom Action Pill Buttons"):hub_code.find("FULL SCREEN EXECUTIVE MODAL")])

print("--- VIEW TAB BAR ---")
print(view_code[:800])
