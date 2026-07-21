import sqlite3

conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
c = conn.cursor()

c.execute("SELECT COUNT(*) FROM requests")
total = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM requests WHERE is_handwritten=1")
hw = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM requests WHERE is_handwritten=0")
not_hw = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM requests WHERE is_handwritten IS NULL")
null_hw = c.fetchone()[0]

print(f"Total rows: {total}")
print(f"is_handwritten=1: {hw}")
print(f"is_handwritten=0: {not_hw}")
print(f"is_handwritten IS NULL: {null_hw}")
