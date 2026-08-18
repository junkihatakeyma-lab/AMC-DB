import sqlite3
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
c = conn.cursor()
c.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='boms'")
print(c.fetchone()[0])
