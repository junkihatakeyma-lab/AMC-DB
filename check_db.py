import sqlite3
import json

conn = sqlite3.connect('db.sqlite3')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("SELECT * FROM requests WHERE request_no='11507'")
r = cur.fetchone()
print('REQUEST:', dict(r) if r else 'Not found')

cur.execute("SELECT * FROM boms WHERE file LIKE '%11507%'")
b = cur.fetchone()
print('BOM:', dict(b) if b else 'Not found')

if b:
    cur.execute("SELECT * FROM components WHERE bom_id = ?", (b['id'],))
    comps = cur.fetchall()
    print('COMPONENTS:', [dict(c) for c in comps])
