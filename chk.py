import sqlite3
c = sqlite3.connect('部品DB.sqlite', timeout=60)
cnt = c.execute("SELECT COUNT(*) FROM previews WHERE file_path LIKE 'data/加工依頼書/%'").fetchone()[0]
print("Previews count:", cnt)
