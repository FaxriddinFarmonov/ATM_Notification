import os

service_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\services\atmService.ts'
with open(service_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'async detail(id: number): Promise<AtmDetailResponse> {',
    'async detail(id: number | string): Promise<AtmDetailResponse> {'
)

with open(service_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("atmService.ts updated to accept number | string for detail!")
