with open('deploy_to_firebase.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "grp['product'] = {'product_code': bdict['product_code'], 'name':" in line:
        lines[i] = "             grp['product'] = {'product_code': bdict['product_code'], 'name': '未登録製品', 'alias': ''}\n"

with open('deploy_to_firebase.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
