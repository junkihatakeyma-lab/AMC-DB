import sqlite3
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT * FROM boms WHERE file LIKE '%3F136.6-0580%'")
bom = c.fetchone()
print('product_code:', bom['product_code'])
