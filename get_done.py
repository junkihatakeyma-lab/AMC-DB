import sqlite3
c = sqlite3.connect('部品DB.sqlite')
res = c.execute("SELECT DISTINCT s.link_key FROM simple_files s JOIN previews p ON s.file_path = p.file_path WHERE s.type='drawing' AND (s.file_path LIKE '%.jww' OR s.file_path LIKE '%.wwj') LIMIT 15").fetchall()
print(", ".join([r[0] for r in res]))
