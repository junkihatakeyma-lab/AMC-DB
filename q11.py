import sqlite3
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT id FROM boms WHERE file LIKE '%3F136.6-0580%'")
bom_id = c.fetchone()['id']
c.execute("SELECT * FROM bom_components WHERE bom_id=?", (bom_id,))
print([dict(r) for r in c.fetchall()])
