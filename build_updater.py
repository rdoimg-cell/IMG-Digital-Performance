"""
Bangun "UPDATE DATA.html" — pengganti UPDATE DATA.bat untuk komputer tanpa Python.
Menyisipkan library SheetJS + template aplikasi ke dalam satu file HTML mandiri.
"""
import base64, os

src = open('updater_src.html', encoding='utf-8').read()
sheetjs = open('/tmp/sheetjs/node_modules/xlsx/dist/xlsx.full.min.js', encoding='utf-8').read()
tpl_b64 = base64.b64encode(open('template.html', 'rb').read()).decode()

html = src.replace('__SHEETJS__', sheetjs).replace('__TEMPLATE_B64__', tpl_b64)

with open('UPDATE DATA.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'✅ UPDATE DATA.html ({os.path.getsize("UPDATE DATA.html")/1024/1024:.2f} MB)')
