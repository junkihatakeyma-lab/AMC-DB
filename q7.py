import sqlite3
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
c = conn.cursor()
c.execute("SELECT id, product_code, new_part_no, file FROM boms WHERE file LIKE '%10972%'")
print('BOMs with 10972:', c.fetchall())
