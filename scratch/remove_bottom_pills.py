path_hub = r"C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\components\analytics\AiBankomatPortalHub.vue"
with open(path_hub, 'r', encoding='utf-8') as f:
    code = f.read()

# Remove Bottom Action Pill Buttons section
start_marker = "<!-- Bottom Action Pill Buttons -->"
end_marker = "<!-- FULL SCREEN EXECUTIVE MODAL"

start_pos = code.find(start_marker)
end_pos = code.find(end_marker)

if start_pos != -1 and end_pos != -1:
    new_code = code[:start_pos] + code[end_pos:]
    with open(path_hub, 'w', encoding='utf-8') as f:
        f.write(new_code)
    print("Successfully removed bottom action buttons section from AiBankomatPortalHub.vue")
else:
    print("Markers not found:", start_pos, end_pos)
