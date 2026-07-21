import sqlite3
c = sqlite3.connect('部品DB.sqlite', timeout=10)
print(c.execute("SELECT COUNT(*) FROM previews").fetchone())
