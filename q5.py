import sqlite3
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT id, product_code, new_part_no, file FROM boms WHERE file LIKE '%3F080SQ-0095%'")
print('BOMs:', [dict(r) for r in c.fetchall()])
c.execute("SELECT request_no, new_part_no FROM requests WHERE request_no='11743'")
print('Requests:', [dict(r) for r in c.fetchall()])
