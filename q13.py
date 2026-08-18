import sqlite3
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT * FROM requests WHERE hinmei LIKE '%IF253-0500%' LIMIT 5")
for r in c.fetchall():
    print(dict(r))
