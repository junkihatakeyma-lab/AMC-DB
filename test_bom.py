import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('部品DB.sqlite')
conn.row_factory = sqlite3.Row

print("Count of IF400=0500:")
print(len(conn.execute("SELECT * FROM boms WHERE product_code LIKE 'IF400=0500%'").fetchall()))
