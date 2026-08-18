import sqlite3
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT id, product_code FROM boms WHERE new_part_no='R0162BSESE0545U1001101001' LIMIT 5")
print('BOMs:', [dict(r) for r in c.fetchall()])
c.execute("SELECT request_no, hinmei, dest, note FROM requests WHERE new_part_no='R0162BSESE0545U1001101001' LIMIT 5")
print('Requests:', [dict(r) for r in c.fetchall()])
