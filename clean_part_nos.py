import sqlite3
import re
import unicodedata

def clean_part_no(text):
    if not isinstance(text, str): return text
    if not text: return text
    
    original = text
    
    # Convert full-width alphanumeric to half-width
    text = unicodedata.normalize('NFKC', text)
    
    # Remove circled numbers at the start (e.g. ①IF220, ①～③ 3F136)
    text = re.sub(r'^[①-⑳][～〜\-\s]*[①-⑳]?\s*', '', text)
    
    # Remove trailing junk like (内)
    text = re.sub(r'\(内\).*?$', '', text)
    text = re.sub(r'（内）.*?$', '', text)
    
    # Remove trailing count like に2ヶ入り
    text = re.sub(r'[ 　]*に[0-9]+ヶ入り.*?$', '', text)
    
    # Remove trailing multiply like ×3
    text = re.sub(r'[ 　]*[x×][ 　]*\d+.*?$', '', text)
    
    # Remove trailing OCR errors for O/I
    text = re.sub(r'[ 　]+[OI01]（[オア][ーイ]）.*?$', '', text)
    text = re.sub(r'[ 　]+[OI01Ō]\s*$', '', text)
    
    # Clean up any trailing spaces
    text = text.strip()
    
    return text

conn = sqlite3.connect('部品DB.sqlite')
c = conn.cursor()

c.execute('SELECT id, part_no FROM bom_components WHERE part_no IS NOT NULL AND part_no != ""')
rows = c.fetchall()

updates = []
for row_id, part_no in rows:
    cleaned = clean_part_no(part_no)
    if cleaned != part_no:
        updates.append((cleaned, row_id))

if updates:
    c.executemany('UPDATE bom_components SET part_no = ? WHERE id = ?', updates)
    conn.commit()
    print(f"Updated {len(updates)} parts in bom_components.")
else:
    print("No parts needed cleaning.")

conn.close()
