import os

path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\views\AtmMonitoringView.vue'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
for i, line in enumerate(lines):
    if 'AtmDetailModal' in line or 'openAtmDetail' in line or 'selectedAtm' in line:
        print(f"{i+1}: {line}")
