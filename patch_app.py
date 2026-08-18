import re

with open('static/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

old_cond = "(c.role === 'ラベル' || c.role === '【特記・赤字】')"
new_cond = "(c.role && (c.role.includes('ラベル') || c.role.includes('赤字') || c.role.includes('特記')))"

if old_cond in text:
    text = text.replace(old_cond, new_cond)
    with open('static/app.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Patched app.js with .includes logic!')
else:
    print('old condition not found!')
