import sqlite3
c = sqlite3.connect('部品DB.sqlite', timeout=10)
print(c.execute("SELECT * FROM previews WHERE file_path LIKE '%KF22-221-1-1.jww'").fetchall())
