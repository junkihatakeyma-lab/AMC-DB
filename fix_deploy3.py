with open('deploy_to_firebase.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "key =" in line and "未" in line:
        lines[i] = "        key = bdict.get('new_part_no') or bdict.get('product_code') or '未分類'\n"
    elif "'product': {'product_code': bdict['product_code'], 'name':" in line and "未" in line:
        lines[i] = "             grp['product'] = {'product_code': bdict['product_code'], 'name': '未登録製品', 'alias': ''}\n"

with open('deploy_to_firebase.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
