import sqlite3
import json
import glob
import sys

c = sqlite3.connect('部品DB.sqlite')
all_parsed = {}
for f in glob.glob('parsed_*.json'):
    try:
        with open(f, 'r', encoding='utf-8') as file:
            all_parsed.update(json.load(file))
    except Exception as e:
        print(f"Error loading {f}: {e}")

boms = dict(c.execute('SELECT file, id FROM boms').fetchall())
inserted = 0

for file_path, parts in all_parsed.items():
    bom_id = boms.get(file_path)
    if bom_id:
        for p in parts:
            c.execute('INSERT INTO bom_components (bom_id, role, part_no, note) VALUES (?,?,?,?)', 
                      (bom_id, p.get('role', ''), p.get('part_no', ''), p.get('note', '')))
        c.execute('UPDATE boms SET layout_ok=1 WHERE id=?', (bom_id,))
        inserted += 1

c.commit()
c.close()
print(f'Inserted {inserted} exception BOMs into bom_components!')
