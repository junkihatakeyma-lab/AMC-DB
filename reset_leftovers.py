import sqlite3

conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM requests WHERE is_handwritten=1 AND hinmei NOT LIKE '[手書き]%' AND hinmei != ''")
leftovers = c.fetchone()[0]
print(f'Leftovers: {leftovers}')

c.execute("UPDATE requests SET hinmei='' WHERE is_handwritten=1 AND hinmei NOT LIKE '[手書き]%' AND hinmei != ''")
conn.commit()
print('Reset leftovers.')
