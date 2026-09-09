import os, re

# 1. Update main.css with white background + dark blue text option rules
css_path = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src\assets\main.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

new_option_css = '''
/* Global Dropdown Option Contrast Fix - Dark Blue Text on White Background */
select option {
  background-color: #ffffff !important;
  color: #0f172a !important;
  padding: 8px 12px !important;
  font-weight: 700 !important;
}

select option:hover,
select option:focus,
select option:active,
select option:checked {
  background-color: #2563eb !important;
  color: #ffffff !important;
}
'''

if 'select option' in css_content:
    # Replace existing select option block
    css_content = re.sub(r'/\* Global Dropdown Option Contrast Fix \*/.*?select option:checked\s*\{[^}]*\}', new_option_css.strip(), css_content, flags=re.DOTALL)
    css_content = re.sub(r'select option\s*\{[^}]*\}.*?select option:checked\s*\{[^}]*\}', new_option_css.strip(), css_content, flags=re.DOTALL)
else:
    css_content += "\n" + new_option_css

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css_content)
print("Updated main.css with dark blue text option rules!")

# 2. Update all vue files to use bg-white text-slate-900 font-bold for options
target_dir = r'C:\Users\Faxriddin\Documents\Frontend-ATM-Informations\src'

for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file.endswith('.vue'):
            full_path = os.path.join(root, file)
            with open(full_path, 'r', encoding='utf-8') as f:
                code = f.read()

            if '<option' in code:
                # Replace any bg-slate-900 or text-white in option class with bg-white text-slate-900
                new_code = re.sub(
                    r'<option([^>]*class=")[^"]*"([^>]*)>',
                    r'<option\1bg-white text-slate-900 font-bold py-1"\2>',
                    code
                )
                # For options without class attribute
                new_code = re.sub(
                    r'<option(?![^>]*class=)([^>]*)>',
                    r'<option class="bg-white text-slate-900 font-bold py-1"\1>',
                    new_code
                )
                if new_code != code:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(new_code)
                    print(f"Updated <option> styling in {file}")

print("All option dropdowns set to dark blue/slate text on white background successfully!")
