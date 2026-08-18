import sqlite3
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
c = conn.cursor()
c.execute("PRAGMA table_info(bom_components)")
for row in c.fetchall():
    print(row)
