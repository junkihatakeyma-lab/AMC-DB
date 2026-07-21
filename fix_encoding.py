import re

with open('static/app.js', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Let's fix the mojibake.
# The mojibake string we saw was `?? uEUŊJ (Excel for Web)</a>`
# Let's find the exact block and replace it manually.

new_block = """                        <div class="action-bar">
                            <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(b.previews))}, ${escapeHtml(JSON.stringify(b.file))})'>プレビュー</button>
                            ${b.sp_url ? `<a href="${b.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (b.file ? `<a href="/${b.file.replace(/\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excelを開く</a>` : '')}
                            ${!b.layout_ok ? `<button class="btn btn-secondary" style="border:1px solid var(--danger);color:var(--danger)" onclick='openAIConfirm(${escapeHtml(JSON.stringify(b))})'>AI解析を確定</button>` : ''}
                        </div>"""

# Replace lines 257 to 261
lines = content.split('\n')

# Find where 'onclick=\'openPreview(' is for BOM
for i, line in enumerate(lines):
    if "openPreview(" in line and "escapeHtml(JSON.stringify(b.previews))" in line:
        # We found the button
        # Let's replace i-1 to i+3
        lines[i-1] = '                        <div class="action-bar">'
        lines[i]   = '                            <button class="btn btn-primary" onclick=\'openPreview(${escapeHtml(JSON.stringify(b.previews))}, ${escapeHtml(JSON.stringify(b.file))})\'>プレビュー</button>'
        lines[i+1] = '                            ${b.sp_url ? `<a href="${b.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (b.file ? `<a href="/${b.file.replace(/\\\\/g, \'/\').split(\'/\').map(encodeURIComponent).join(\'/\')}" target="_blank" class="btn btn-secondary">Excelを開く</a>` : \'\')}'
        lines[i+2] = '                            ${!b.layout_ok ? `<button class="btn btn-secondary" style="border:1px solid var(--danger);color:var(--danger)" onclick=\'openAIConfirm(${escapeHtml(JSON.stringify(b))})\'>AI解析を確定</button>` : \'\'}'
        lines[i+3] = '                        </div>'
        break

# We also need to fix the other buttons that got mojibaked if there are any.
# "Excelを開く" became "ExcelJ"
for i in range(len(lines)):
    lines[i] = lines[i].replace("ExcelJ", "Excelを開く")
    lines[i] = lines[i].replace("AI͂m", "AI解析を確定")
    lines[i] = lines[i].replace("?? uEUŊJ", "🌐 ブラウザで開く")

with open('static/app.js', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
    
print("Fixed app.js using python.")
