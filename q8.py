import sqlite3
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
c = conn.cursor()
c.execute("SELECT file, new_part_no FROM boms WHERE product_code='3F136' LIMIT 10")
for r in c.fetchall():
    print(r)
