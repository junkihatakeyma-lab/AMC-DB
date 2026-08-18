from migrate_to_25digit import normalize_text, compute_score
import json
import sqlite3
import re

def extract_pleat_counts(text):
    if not text: return []
    matches = re.findall(r'(\d+)山|山数(\d+)', text)
    pleats = []
    for m in matches:
        if m[0]: pleats.append(m[0])
        elif m[1]: pleats.append(m[1])
    return list(set(pleats))

def safe_compute_score(new_id, old_id, spec, text, explicit_filename=""):
    score = compute_score(new_id, old_id, spec, text, explicit_filename)
    
    text_norm = normalize_text(text)
    full_text = text_norm + " " + normalize_text(explicit_filename) if explicit_filename else text_norm
    found_pleats = extract_pleat_counts(full_text)
    
    if len(new_id) == 25:
        pleat_count_str = new_id[19:22]
        if pleat_count_str.isdigit():
            pleat_val = str(int(pleat_count_str))
            if found_pleats and pleat_val not in found_pleats:
                return -9999
                
    return score

conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute("SELECT id, file FROM boms WHERE file LIKE '%IF402B-0545(100山%'")
row = c.fetchone()
bom_id = row['id']
filename = row['file']

c.execute("SELECT part_no, role FROM bom_components WHERE bom_id = ?", (bom_id,))
comps = c.fetchall()
bom_text = ' '.join(f"{comp['part_no']} {comp['role']}" for comp in comps)

with open('mapping.json', 'r', encoding='utf-8') as f:
    mapping = json.load(f)

scores = []
for m in mapping:
    if 'IF402B-0545' in m['old_id']:
        score = safe_compute_score(m['new_id'], m['old_id'], m['spec'], bom_text, filename)
        scores.append((score, m['new_id'], m['spec']))

scores.sort(reverse=True, key=lambda x: x[0])
for s in scores:
    print(f"{s[0]} - {s[1]} - {s[2]}")
