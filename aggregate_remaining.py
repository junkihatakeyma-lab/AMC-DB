import sqlite3
import json
import glob

c = sqlite3.connect('部品DB.sqlite')
all_parsed = {}
for f in glob.glob('parsed_*.json'):
    try:
        with open(f, 'r', encoding='utf-8') as file:
            all_parsed.update(json.load(file))
    except Exception as e:
        pass

boms = dict(c.execute('SELECT file, id FROM boms').fetchall())
inserted = 0

for file_path, parts in all_parsed.items():
    # fix double backslash
    fixed_path = file_path.replace('\\\\', '\\')
    bom_id = boms.get(fixed_path)
    
    # Also check if it's already layout_ok=1 so we don't insert duplicates
    if bom_id:
        is_ok = c.execute('SELECT layout_ok FROM boms WHERE id=?', (bom_id,)).fetchone()[0]
        if not is_ok:
            for p in parts:
                c.execute('INSERT INTO bom_components (bom_id, role, part_no, note) VALUES (?,?,?,?)', 
                          (bom_id, p.get('role', ''), p.get('part_no', ''), p.get('note', '')))
            c.execute('UPDATE boms SET layout_ok=1 WHERE id=?', (bom_id,))
            inserted += 1

c.commit()
c.close()
print(f'Inserted {inserted} MORE exception BOMs into bom_components!')
