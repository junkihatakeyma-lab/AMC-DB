import sqlite3

conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
c = conn.cursor()

c.execute("SELECT COUNT(*) FROM requests WHERE hinmei LIKE '[手書き] %'")
print('Starts with [手書き] :', c.fetchone()[0])

c.execute("SELECT COUNT(*) FROM requests WHERE is_handwritten=1 AND hinmei != ''")
print('Handwritten non-empty:', c.fetchone()[0])

c.execute("SELECT COUNT(*) FROM requests WHERE is_handwritten=1 AND hinmei = ''")
print('Handwritten empty:', c.fetchone()[0])
