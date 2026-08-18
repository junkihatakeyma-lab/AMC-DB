import sqlite3
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM boms WHERE product_code='4F162-0545'")
print('Total BOMs with 4F162-0545:', c.fetchone()[0])
c.execute("SELECT product_code, COUNT(*) FROM boms GROUP BY product_code ORDER BY COUNT(*) DESC LIMIT 5")
print('Top 5 BOMs by product_code:', c.fetchall())

c.execute("SELECT COUNT(*) FROM boms WHERE new_part_no='R0162BSESE0545U1001101001'")
print('Total BOMs mapped to R0162:', c.fetchone()[0])

c.execute("SELECT new_part_no, COUNT(*) FROM requests GROUP BY new_part_no ORDER BY COUNT(*) DESC LIMIT 5")
print('Top 5 requests by new_part_no:', c.fetchall())
