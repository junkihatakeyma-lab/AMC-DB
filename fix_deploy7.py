with open('deploy_to_firebase.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "print(" in line:
        lines[i] = "\n"

with open('deploy_to_firebase.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
