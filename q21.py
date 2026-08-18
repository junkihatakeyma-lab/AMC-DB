import sqlite3

conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute("SELECT new_part_no, COUNT(*) as count FROM boms WHERE new_part_no LIKE 'R0203ASESE0545U%' GROUP BY new_part_no")
rows = c.fetchall()

for r in rows:
    print(f"{r['new_part_no']} : {r['count']} BOMs")
