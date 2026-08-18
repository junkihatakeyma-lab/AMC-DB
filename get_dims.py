import sqlite3
import json

conn = sqlite3.connect('部品DB.sqlite')
c = conn.cursor()

c.execute('''
    SELECT id, role, part_no, note
    FROM bom_components
    WHERE part_no LIKE '%φ%' OR part_no LIKE '%Φ%' 
       OR part_no LIKE '%=%' OR part_no LIKE '%=%'
       OR (part_no GLOB '*[0-9]x[0-9]*' OR part_no GLOB '*[0-9]X[0-9]*')
       OR part_no LIKE '%t=%' OR part_no LIKE 't%'
''')

rows = c.fetchall()
out = []
for row in rows:
    out.append({
        'id': row[0],
        'role': row[1],
        'part_no': row[2],
        'note': row[3]
    })

with open('dim_parts.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

conn.close()
