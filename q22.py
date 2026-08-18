import sqlite3
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT id FROM boms WHERE file LIKE '%IF402B-0545(100山%'")
row = c.fetchone()
if row:
    bom_id = row['id']
    c.execute("SELECT part_no, role FROM bom_components WHERE bom_id = ?", (bom_id,))
    comps = c.fetchall()
    bom_text = ' '.join(f"{comp['part_no']} {comp['role']}" for comp in comps)
    print('bom_text:', bom_text.encode('utf-8'))
else:
    print("Not found")
