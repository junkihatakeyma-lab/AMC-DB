import sqlite3

c = sqlite3.connect('部品DB.sqlite', timeout=10)
res = c.execute("SELECT preview_path FROM previews WHERE file_path LIKE 'data/加工依頼書/%' LIMIT 1").fetchone()
print(res)
