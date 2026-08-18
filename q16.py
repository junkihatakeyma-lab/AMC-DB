import sqlite3
import json
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT id FROM boms WHERE file LIKE '%3F136.6-0580%'")
bom_id = c.fetchone()['id']

c.execute("SELECT part_no, role FROM bom_components WHERE bom_id = ?", (bom_id,))
comps = c.fetchall()
comp_strs = [f"{comp['part_no']} {comp['role']}" for comp in comps]
bom_text = " ".join(comp_strs)
print('BOM text:', bom_text.encode('utf-8'))
