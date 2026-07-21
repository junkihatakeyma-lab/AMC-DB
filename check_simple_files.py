import sqlite3

conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
c = conn.cursor()

c.execute("SELECT type, COUNT(*) FROM simple_files GROUP BY type")
for row in c.fetchall():
    print(f"type: {row[0]}, count: {row[1]}")
