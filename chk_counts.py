import sqlite3
import json
import glob

conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM requests WHERE hinmei != ''")
total_db = c.fetchone()[0]

count_json = 0
for f in glob.glob('parsed_*.json'):
    with open(f, 'r', encoding='utf-8') as file:
        data = json.load(file)
        if isinstance(data, list): count_json += len(data)

print(f"Total in JSON: {count_json}")
print(f"Total non-empty in DB: {total_db}")
