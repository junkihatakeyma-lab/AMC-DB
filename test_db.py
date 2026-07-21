import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('部品DB.sqlite')
conn.row_factory = sqlite3.Row

# Get preview rows for inspections
res = conn.execute("SELECT file_path, preview_path FROM previews WHERE file_path LIKE '%検査証%' LIMIT 5").fetchall()
for row in res:
    print(dict(row))

# Check how many inspection previews there are
count = conn.execute("SELECT COUNT(*) as c FROM previews WHERE file_path LIKE '%検査証%'").fetchone()['c']
print(f"Total inspection previews: {count}")

# Check simple_files for inspections
res2 = conn.execute("SELECT file_path FROM simple_files WHERE type='inspection' LIMIT 5").fetchall()
print("simple_files:")
for row in res2:
    print(dict(row))
