import sqlite3
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT file, product_code FROM boms WHERE file LIKE '%3F136%'")
for r in c.fetchall():
    print(r['file'], r['product_code'])
