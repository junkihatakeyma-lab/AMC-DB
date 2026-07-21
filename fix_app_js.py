import re

with open('static/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace b.file
content = re.sub(
    r'\$\{b\.file \? `<a href="/\$\{b\.file\.replace\([^}]+\}" target="_blank" class="btn btn-secondary">Excelを開く</a>` : \'\'\}',
    r'${b.sp_url ? `<a href="${b.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (b.file ? `<a href="/${b.file.replace(/\\\\/g, \'/\').split(\'/\').map(encodeURIComponent).join(\'/\')}" target="_blank" class="btn btn-secondary">Excelを開く</a>` : \'\')}',
    content
)

# Replace r.file
content = re.sub(
    r'\$\{r\.file \? `<a href="/\$\{r\.file\.replace\([^}]+\}" target="_blank" class="btn btn-secondary">Excelを開く</a>` : \'\'\}',
    r'${r.sp_url ? `<a href="${r.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (r.file ? `<a href="/${r.file.replace(/\\\\/g, \'/\').split(\'/\').map(encodeURIComponent).join(\'/\')}" target="_blank" class="btn btn-secondary">Excelを開く</a>` : \'\')}',
    content
)

# Replace cache buster to force reload
content = content.replace("app.js?v=6", "app.js?v=7")

with open('static/app.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated app.js successfully.")
