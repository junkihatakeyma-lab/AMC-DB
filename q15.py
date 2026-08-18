import sqlite3
import json
conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT * FROM boms WHERE file LIKE '%3F136.6-0580%'")
bom = c.fetchone()
print("BOM text:")
print(bom['text'])

# Check what matched
with open('mapping.json', 'r', encoding='utf-8') as f:
    mapping = json.load(f)

for m in mapping:
    if m['new_id'] == 'R0137ADMSU0951X1101052001':
        print("\nMaster spec:", m['spec'])
        break
