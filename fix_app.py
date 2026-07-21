import re

with open('static/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r"\.split\('/'\)\.pop\(\)", r".replace(/\\\\/g, '/').split('/').pop()", content)
content = re.sub(r"\.split\('/'\)\.map\(encodeURIComponent\)\.join\('/'\)", r".replace(/\\\\/g, '/').split('/').map(encodeURIComponent).join('/')", content)

content = content.replace('<img src="/${p.file_path}"', '<img src="/${p.file_path.replace(/\\\\/g, \'/\').split(\'/\').map(encodeURIComponent).join(\'/\')}"')

old_modal_logic = '''    if (!previews || previews.length === 0) {
        modalBody.innerHTML = '<div style="text-align:center;padding:2rem">プレビュー画像がありません（PDF変換待ち、または未生成です）</div>';
    } else {'''

new_modal_logic = '''    if (!previews || previews.length === 0 || previews[0] === 'previews/dummy_0.png') {
        modalBody.innerHTML = '<div style="text-align:center;padding:2rem">プレビュー画像がありません（PDF変換待ち、または未生成です）</div>';
    } else {'''

content = content.replace(old_modal_logic, new_modal_logic)

with open('static/app.js', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed app.js')
