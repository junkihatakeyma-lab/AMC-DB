import sqlite3
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT * FROM requests WHERE request_no='10972'")
print('Request 10972:', [dict(r) for r in c.fetchall()])
c.execute("SELECT * FROM bom_requests WHERE request_no='10972'")
print('bom_requests 10972:', [dict(r) for r in c.fetchall()])
