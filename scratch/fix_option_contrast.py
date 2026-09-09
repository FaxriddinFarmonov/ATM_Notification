import os, re

# 1. Update main.css with global select/option contrast rules
css_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\assets\main.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

option_css = '''
/* Global Dropdown Option Contrast Fix */
select option {
  background-color: #0f172a !important;
  color: #f8fafc !important;
  padding: 8px 12px !important;
  font-weight: 700 !important;
}

select option:hover,
select option:focus,
select option:active,
select option:checked {
  background-color: #1e293b !important;
  color: #38bdf8 !important;
}
'''

if 'select option' not in css_content:
    css_content += "\n" + option_css
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css_content)
    print("Updated main.css with option dropdown rules!")

# 2. Update all vue files to ensure option tags have dark bg and crisp white text
target_dir = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src'

for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file.endswith('.vue'):
            full_path = os.path.join(root, file)
            with open(full_path, 'r', encoding='utf-8') as f:
                code = f.read()

            if '<option' in code:
                # Add bg-slate-900 text-white to option tags if missing
                new_code = re.sub(
                    r'<option(?![^>]*class=)([^>]*)>',
                    r'<option class="bg-slate-900 text-white font-bold py-1"\1>',
                    code
                )
                if new_code != code:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(new_code)
                    print(f"Updated <option> styling in {file}")

print("All dropdown option styles fixed successfully!")
