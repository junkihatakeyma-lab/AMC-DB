import sqlite3
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
c = conn.cursor()
c.execute("SELECT file FROM boms WHERE file LIKE '%IF100-1000%'")
for row in c.fetchall():
    print(row[0])
