with open('deploy_to_firebase.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
new_lines = []
for line in lines:
    if line.strip() != 'pass':
        new_lines.append(line)

with open('deploy_to_firebase.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
