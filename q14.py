import sqlite3
import re
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT * FROM requests WHERE new_part_no IS NOT NULL LIMIT 5")
for r in c.fetchall():
    print(r['request_no'], r['hinmei'], r['new_part_no'])
