import sqlite3
import re
import json

DB_PATH = '部品DB.sqlite'

def clean_part_no(p):
    if not p: return p
    p = p.replace('：', ':')
    m = re.match(r'^(?:[①-⑳]?\s*[A-Z]\s*:)(.*)$', p)
    if m:
        return m.group(1).strip()
    return p

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("SELECT id, part_no FROM bom_components")
rows = c.fetchall()

updates = 0
for row_id, p in rows:
    cleaned = clean_part_no(p)
    if cleaned != p:
        c.execute("UPDATE bom_components SET part_no = ? WHERE id = ?", (cleaned, row_id))
        updates += 1

conn.commit()
print(f"Updated {updates} part numbers in bom_components.")

# Also update simple_files if they exist
try:
    c.execute("SELECT id, link_key FROM simple_files")
    rows = c.fetchall()
    updates_simple = 0
    for row_id, key in rows:
        cleaned = clean_part_no(key)
        if cleaned != key:
            c.execute("UPDATE simple_files SET link_key = ? WHERE id = ?", (cleaned, row_id))
            updates_simple += 1
    conn.commit()
    print(f"Updated {updates_simple} link_keys in simple_files.")
except sqlite3.OperationalError:
    print("table simple_files does not exist, skipping.")

conn.close()
