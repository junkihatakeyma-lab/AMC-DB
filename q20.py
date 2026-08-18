import sqlite3
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
c = conn.cursor()
c.execute("SELECT file, new_part_no FROM boms WHERE file LIKE '%3F136%'")
for r in c.fetchall():
    print(r)
