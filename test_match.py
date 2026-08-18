import sqlite3
import pandas as pd
import re

# Load Parts Master
df_master = pd.read_excel('data/部品マスタ/部品マスタ.xlsx')
master_parts = df_master['品番・図番'].dropna().tolist()

# Load DB Parts
conn = sqlite3.connect('部品DB.sqlite')
db_parts = [r[0] for r in conn.execute('SELECT DISTINCT part_no FROM bom_components WHERE part_no IS NOT NULL').fetchall()]
conn.close()

def normalize(text):
    if not isinstance(text, str):
        return ""
    # Convert to uppercase
    text = text.upper()
    # Remove all non-alphanumeric (keep only A-Z and 0-9)
    text = re.sub(r'[^A-Z0-9]', '', text)
    return text

# Create normalized dicts
norm_master = {normalize(p): p for p in master_parts if normalize(p)}

matches = []
for db_p in db_parts:
    norm_db = normalize(db_p)
    if not norm_db:
        continue
    
    # Try exact match first on normalized string
    if norm_db in norm_master:
        matches.append((db_p, norm_master[norm_db]))
        continue
    
    # Try finding the DB part inside the Master part
    # e.g. norm_db = 'IF4000600E', master = '511IF4000600E'
    # To avoid false positives, require norm_db to be at least 5 chars
    if len(norm_db) >= 5:
        for m_norm, m_orig in norm_master.items():
            if norm_db in m_norm:
                matches.append((db_p, m_orig))
                break

print(f"Total DB Parts: {len(db_parts)}")
print(f"Matched DB Parts: {len(matches)}")
print("Sample matches:")
for m in matches[:20]:
    print(f"  DB: {m[0]:<20} -> Master: {m[1]}")
