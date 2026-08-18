import sqlite3
import re
from collections import Counter

conn = sqlite3.connect('部品DB.sqlite')
c = conn.cursor()
c.execute("SELECT part_no FROM bom_components WHERE part_no LIKE '%:%' OR part_no LIKE '%：%'")
rows = c.fetchall()

prefixes = Counter()
for row in rows:
    p = row[0]
    if p:
        m = re.match(r'^(.*?)[：:]', p)
        if m:
            prefixes[m.group(1).strip()] += 1
print(prefixes.most_common(50))
conn.close()
