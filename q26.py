import sqlite3
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT file FROM boms WHERE new_part_no = 'R0175ASEJU1003U1001045001'")
for row in c.fetchall():
    print(row['file'])
