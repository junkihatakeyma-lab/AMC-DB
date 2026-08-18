import codecs

with open('deploy_to_firebase.py', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

# Find normalize_text and replace it completely
start_idx = -1
for i, line in enumerate(lines):
    if line.startswith('def normalize_text'):
        start_idx = i
        break

if start_idx != -1:
    end_idx = start_idx + 1
    while end_idx < len(lines) and (lines[end_idx].startswith('    ') or lines[end_idx].strip() == ''):
        end_idx += 1
    new_func = '''def normalize_text(text) -> str:
    text = safe_str(text)
    if not text:
        return ""
    text = text.lower()
    text = text.translate(str.maketrans(
        'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ０１２３４５６７８９',
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    ))
    return text
'''
    lines[start_idx:end_idx] = [new_func]

# Fix line 81 which had '未刁EEEE,'
for i, line in enumerate(lines):
    if "'new_part_no':" in line and "未" in line:
        lines[i] = "        'new_part_no': '未分類',\n"
    if "def deploy():" in line:
        break # We don't care about anything after this since it's just print statements

with open('deploy_to_firebase.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

import py_compile
py_compile.compile('deploy_to_firebase.py')
print("Fixed successfully!")
with open('deploy_to_firebase.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if \"key = \" in line and \"��\" in line:
        lines[i] = \"        key = '������'\\n\"
with open('deploy_to_firebase.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Fixed line 90!')
