path = r"d:\PycharmProjects\Bankomat_Notification_bot\apps\Bankomat_hisobot\services\region_analytics.py"
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

# Fix in _yearly
old_yearly_block = """            yearly_data[year]["btech"] += (
                costs["btech"]
            )

            yearly_data[year]["glob"] += (
                costs["glob"]
            )

            yearly_data[year]["incassation"] += (
                costs["incassation"]
            )

            yearly_data[year]["rent"] += (
                costs["rent"]
            )

            yearly_data[year]["electricity"] += (
                costs["electricity"]
            )

            yearly_data[year]["maintenance"] += (
                costs["maintenance"]
            )

            yearly_data[year]["total_expense"] += (
                costs["total_expense"]
            )

            yearly_data[year]["net_result"] += (
                income
                - costs["total_expense"]
            )"""

new_yearly_block = """            yearly_data[year]["btech"] += Decimal(str(costs["btech"]))
            yearly_data[year]["glob"] += Decimal(str(costs["glob"]))
            yearly_data[year]["incassation"] += Decimal(str(costs["incassation"]))
            yearly_data[year]["rent"] += Decimal(str(costs["rent"]))
            yearly_data[year]["electricity"] += Decimal(str(costs["electricity"]))
            yearly_data[year]["maintenance"] += Decimal(str(costs["maintenance"]))
            yearly_data[year]["total_expense"] += Decimal(str(costs["total_expense"]))
            yearly_data[year]["net_result"] += (
                income - Decimal(str(costs["total_expense"]))
            )"""

if old_yearly_block in code:
    code = code.replace(old_yearly_block, new_yearly_block)
    print("Replaced yearly_block successfully")
else:
    print("old_yearly_block NOT found exactly, doing fuzzy match...")
    # Replace individual lines
    code = code.replace('yearly_data[year]["btech"] += (\n                costs["btech"]\n            )', 'yearly_data[year]["btech"] += Decimal(str(costs["btech"]))')
    code = code.replace('yearly_data[year]["glob"] += (\n                costs["glob"]\n            )', 'yearly_data[year]["glob"] += Decimal(str(costs["glob"]))')
    code = code.replace('yearly_data[year]["incassation"] += (\n                costs["incassation"]\n            )', 'yearly_data[year]["incassation"] += Decimal(str(costs["incassation"]))')
    code = code.replace('yearly_data[year]["rent"] += (\n                costs["rent"]\n            )', 'yearly_data[year]["rent"] += Decimal(str(costs["rent"]))')
    code = code.replace('yearly_data[year]["electricity"] += (\n                costs["electricity"]\n            )', 'yearly_data[year]["electricity"] += Decimal(str(costs["electricity"]))')
    code = code.replace('yearly_data[year]["maintenance"] += (\n                costs["maintenance"]\n            )', 'yearly_data[year]["maintenance"] += Decimal(str(costs["maintenance"]))')
    code = code.replace('yearly_data[year]["total_expense"] += (\n                costs["total_expense"]\n            )', 'yearly_data[year]["total_expense"] += Decimal(str(costs["total_expense"]))')
    code = code.replace('income\n                - costs["total_expense"]', 'income - Decimal(str(costs["total_expense"]))')

with open(path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved region_analytics.py fix")
