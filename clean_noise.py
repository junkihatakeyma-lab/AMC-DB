import sqlite3
import re

def clean_noise():
    conn = sqlite3.connect('部品DB.sqlite')
    c = conn.cursor()

    c.execute('''
        SELECT id, role, part_no, note
        FROM bom_components
        WHERE part_no IS NOT NULL AND part_no != ''
          AND role NOT LIKE '%ラベル%'
          AND role NOT LIKE '%赤字%'
          AND role NOT LIKE '%特記%'
          AND role NOT LIKE '%検査表%'
          AND role NOT LIKE '%荷札%'
          AND role NOT LIKE '%袋%'
          AND role NOT LIKE '%外装箱%'
          AND part_no NOT IN (SELECT db_part_no FROM part_master_links)
    ''')
    unlinked = c.fetchall()

    updates = []
    
    for r in unlinked:
        db_id, role, p, note = r
        p_str = str(p)
        note_str = str(note) if note else ""
        original_p = p_str
        
        needs_update = False
        
        # 1. Clean up "O(オー)", "I(アイ)", etc.
        # Often it looks like " O(オー)" or "O(ｵｰ)" or "I(ｱｲ)"
        match_oi = re.search(r'\s*[OI]\s*\([^\)]*\)', p_str)
        if match_oi:
            oi_text = match_oi.group(0)
            p_str = p_str.replace(oi_text, '').strip()
            note_str = f"{note_str} / {oi_text.strip()}".strip(' /')
            needs_update = True
            
        # 2. Check if the remaining part_no is still just noise (Kana or Brackets)
        if re.search(r'[ぁ-んァ-ヶ]', p_str) or re.search(r'^[\(\)\s\?\[\]]+$', p_str) or p_str == 'IF' or p_str == '1A':
            # It's noise, move entirely to note
            note_str = f"{note_str} / {p_str}".strip(' /')
            p_str = ""
            needs_update = True

        if needs_update:
            updates.append((p_str, note_str, db_id))

    print(f"Found {len(updates)} noisy records to fix.")
    
    c.executemany('''
        UPDATE bom_components
        SET part_no = ?, note = ?
        WHERE id = ?
    ''', updates)

    conn.commit()
    conn.close()
    print("Database updated.")

if __name__ == '__main__':
    clean_noise()
