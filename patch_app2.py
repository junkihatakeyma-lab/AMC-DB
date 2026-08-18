import re

with open('static/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

old_cond = "(c.role && (c.role.includes('ラベル') || c.role.includes('赤字') || c.role.includes('特記')))"
new_cond = "(c.role && (c.role.includes('ラベル') || c.role.includes('赤字') || c.role.includes('特記') || c.role.includes('検査表') || c.role.includes('荷札') || c.role.includes('ビニール袋') || c.role.includes('袋')))"

if old_cond in text:
    text = text.replace(old_cond, new_cond)
    with open('static/app.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated app.js')
else:
    print('Could not find old_cond in app.js')
