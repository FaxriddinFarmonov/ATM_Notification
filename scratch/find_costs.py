path = r"d:\PycharmProjects\Bankomat_Notification_bot\apps\Bankomat_hisobot\services\region_analytics.py"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines, start=1):
    if "_period_costs" in line:
        print(f"L{idx}: {line.strip()}")
