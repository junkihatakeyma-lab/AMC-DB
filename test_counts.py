import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('部品DB.sqlite')
conn.row_factory = sqlite3.Row

print(f"BOMs: {conn.execute('SELECT COUNT(*) FROM boms').fetchone()[0]}")
print(f"Reqs: {conn.execute('SELECT COUNT(*) FROM requests').fetchone()[0]}")
print(f"Insps: {conn.execute(\"SELECT COUNT(*) FROM simple_files WHERE type='inspection'\").fetchone()[0]}")
print(f"Photos: {conn.execute(\"SELECT COUNT(*) FROM simple_files WHERE type='photo'\").fetchone()[0]}")
print(f"Drawings: {conn.execute(\"SELECT COUNT(*) FROM simple_files WHERE type='drawing'\").fetchone()[0]}")
