with open('deploy_to_firebase.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "if rdict.get('file') and rdict['file'].startswith('data/" in line:
        if "elif" in line:
            lines[i] = "        elif rdict.get('file') and rdict['file'].startswith('data/加工依頼書'):\n"
        else:
            lines[i] = "        if rdict.get('file') and rdict['file'].startswith('data/加工依頼書_手書き'):\n"

with open('deploy_to_firebase.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
