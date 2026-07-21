import sqlite3
c = sqlite3.connect('部品DB.sqlite')
print(c.execute("SELECT preview_path FROM previews WHERE file_path LIKE '%KF26-230-1%'").fetchall())
