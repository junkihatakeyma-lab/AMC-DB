import sqlite3
import re
import unicodedata

def normalize(text):
    if not isinstance(text, str): return ""
    # Convert full-width to half-width
    text = unicodedata.normalize('NFKC', text)
    # Remove circled numbers (1-20)
    text = re.sub(r'[①-⑳]', '', text)
    # Remove common extra trailing phrases
    text = re.sub(r'\(内\).*?$', '', text)
    text = re.sub(r'に\d+ヶ入り.*?$', '', text)
    text = re.sub(r'×\s*\d+.*?$', '', text)
    text = re.sub(r'[OI]（[オア][ーイ]）.*?$', '', text) # O(オー), I(アイ)
    # Convert to upper and strip symbols
    text = text.upper()
    text = re.sub(r'[^A-Z0-9]', '', text)
    return text

conn = sqlite3.connect('部品DB.sqlite')
c = conn.cursor()

# Get all unlinked parts
c.execute('''
    SELECT DISTINCT part_no
    FROM bom_components
    WHERE part_no IS NOT NULL AND part_no != ''
      AND role != 'ラベル' AND role != '【特記・赤字】'
      AND part_no NOT IN (SELECT db_part_no FROM part_master_links)
''')
unlinked = [r[0] for r in c.fetchall()]

# Get all master parts
c.execute("SELECT master_id FROM parts_master")
master_parts = [r[0] for r in c.fetchall()]
norm_master = {normalize(p): p for p in master_parts if normalize(p)}

new_matches = 0
for p in unlinked:
    norm = normalize(p)
    if not norm: continue
    if norm in norm_master:
        new_matches += 1
    elif len(norm) >= 5:
        for m_norm in norm_master:
            if norm in m_norm:
                new_matches += 1
                break

print(f"By using smart normalize, we could automatically link {new_matches} MORE parts out of the {len(unlinked)} unlinked parts!")
conn.close()
