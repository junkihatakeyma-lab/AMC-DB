from migrate_to_25digit import compute_score
import json
import sqlite3

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
        score = compute_score(m['new_id'], m['old_id'], m['spec'], bom_text, filename)
        scores.append((score, m['new_id'], m['spec']))

scores.sort(reverse=True, key=lambda x: x[0])
for s in scores:
    print(f"{s[0]} - {s[1]} - {s[2]}")
