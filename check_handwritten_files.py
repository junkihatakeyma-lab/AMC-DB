import sqlite3

conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
c = conn.cursor()
c.execute("SELECT file, request_no FROM requests WHERE is_handwritten=1 LIMIT 5")
for row in c.fetchall():
    print(row)
