import re

def normalize_text(t):
    if not t: return ""
    return str(t).lower().replace(' ', '').replace('　', '')

def extract_pleat_counts(text):
    if not text: return []
    # Match patterns like 100山, 山数100
    matches = re.findall(r'(\d+)山|山数(\d+)', text)
    pleats = []
    for m in matches:
        if m[0]: pleats.append(m[0])
        elif m[1]: pleats.append(m[1])
    return list(set(pleats))

bom_filename = "IF402B-0545(100山#12004).xlsx"
bom_text = "IF402-001 プレートA IF402B-002 プレートB IF402B-004-0545 チューブ IF220-007F P/K 14F200-0545 外装箱 ラベル 【特記・赤字】"

full_text = normalize_text(bom_text) + " " + normalize_text(bom_filename)
found_pleats = extract_pleat_counts(full_text)
print(found_pleats)
