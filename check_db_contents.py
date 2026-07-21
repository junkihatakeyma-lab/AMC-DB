import sqlite3

conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
c = conn.cursor()

c.execute("SELECT request_no, hinmei FROM requests WHERE is_handwritten=1 AND hinmei NOT LIKE '[手書き] %' LIMIT 10")
for row in c.fetchall():
    print(row)
