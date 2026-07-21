import sqlite3
c = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite').cursor()
print(c.execute("SELECT count(*) FROM requests WHERE is_handwritten=1 AND hinmei!=''").fetchone()[0])
