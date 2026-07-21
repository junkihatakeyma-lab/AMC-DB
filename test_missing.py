import sqlite3
import os

conn = sqlite3.connect('部品DB.sqlite')
c = conn.cursor()
c.execute("SELECT file_path FROM simple_files WHERE type='drawing' AND file_path NOT IN (SELECT file_path FROM previews)")
missing = c.fetchall()

exts = {}
for f in missing:
    ext = os.path.splitext(f[0])[1].lower()
    exts[ext] = exts.get(ext, 0) + 1

print("Missing previews by extension:", exts)
