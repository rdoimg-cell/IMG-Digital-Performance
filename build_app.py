"""
Gabungkan template.html + data.json  ->  ask_img_analytics.html
Jalankan setiap kali data di-update:  python3 build_data.py && python3 build_app.py
"""
import json, os

data = open('data.json', encoding='utf-8').read()
tpl = open('template.html', encoding='utf-8').read()

if '__DATA__' not in tpl:
    raise SystemExit('❌ template.html tidak punya placeholder __DATA__')

html = tpl.replace('__DATA__', data)

with open('ask_img_analytics.html', 'w', encoding='utf-8') as f:
    f.write(html)

# index.html supaya GitHub Pages otomatis membukanya
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

size = os.path.getsize('ask_img_analytics.html') / 1024
print(f'✅ ask_img_analytics.html  ({size:.0f} KB)')
print(f'✅ index.html              (salinan untuk GitHub Pages)')
