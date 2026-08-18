import sqlite3
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM boms WHERE new_part_no IS NOT NULL AND file LIKE '%(#%)%'")
print(c.fetchone()[0])
