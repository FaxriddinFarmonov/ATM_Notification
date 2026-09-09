import os
import re

src_dir = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src'

single_quote_pattern = re.compile(r"'[^'\n]*'[^'\n]*'")

found_errors = []

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(('.ts', '.js', '.vue')):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for idx, line in enumerate(lines, 1):
                # Check for pattern like '... ro'yxat ...'
                if re.search(r"'\w+ ro'yxat", line) or re.search(r"'\w+ o'zg", line) or re.search(r"'\w+ bo'l", line) or re.search(r"'\w+ qo'sh", line) or re.search(r"'\w+ to'g", line):
                    found_errors.append((path, idx, line.strip()))

print(f"Found {len(found_errors)} potential quote issues:")
for p, l, line in found_errors:
    print(f"{p}:{l} -> {line}")
