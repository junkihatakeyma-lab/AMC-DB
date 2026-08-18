import sqlite3
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT * FROM bom_requests WHERE bom_id IN (SELECT id FROM boms WHERE new_part_no='R0162BSESE0545U1001101001')")
print('BOM Requests for R0162:', [dict(r) for r in c.fetchall()])
