with open('deploy_to_firebase.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "key = bdict.get('new_part_no') or bdict.get('product_code') or" in line:
        lines[i] = "        key = bdict.get('new_part_no') or bdict.get('product_code') or '未分類'\n"
    elif "if not target.get('product') and key !=" in line:
        lines[i] = "        if not target.get('product') and key != '未分類':\n"
    elif "target['product'] = {'product_code': key, 'name':" in line:
        lines[i] = "            target['product'] = {'product_code': key, 'name': '未登録部品', 'alias': ''}\n"

with open('deploy_to_firebase.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
