import sqlite3
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM requests WHERE hinmei LIKE '[手書き]%'")
print('OCR processed records starting with [手書き]:', c.fetchone()[0])
