import sqlite3

conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
c = conn.cursor()
c.execute("SELECT * FROM previews WHERE file_path LIKE 'data/加工依頼書_手書き%' LIMIT 5")
for row in c.fetchall():
    print(row)
