import sqlite3
import re

def fix_dimensions():
    conn = sqlite3.connect('部品DB.sqlite')
    c = conn.cursor()

    # Query to find parts that are actually dimensions
    c.execute('''
        SELECT id, role, part_no, note
        FROM bom_components
        WHERE part_no LIKE '%φ%' OR part_no LIKE '%Φ%' 
           OR part_no LIKE '%=%'
           OR (part_no GLOB '*[0-9]x[0-9]*' OR part_no GLOB '*[0-9]X[0-9]*')
           OR part_no LIKE '%t=%' OR part_no LIKE 't%' OR part_no LIKE '%ｔ%'
    ''')
    rows = c.fetchall()

    updates = []
    for row in rows:
        db_id, role, part_no, note = row
        
        # Ensure they are strings
        role_str = str(role) if role else ""
        part_str = str(part_no) if part_no else ""
        note_str = str(note) if note else ""

        # Skip if part_no doesn't actually contain typical dimension characters (safety check)
        if not re.search(r'(φ|Φ|=|x|X|t|ｔ|×)', part_str):
            continue

        # Check if part_str is REALLY a dimension or maybe a real part number that just has 't' or 'X' in it?
        # Typically real part numbers have '-' in them.
        if re.search(r'[A-Z0-9]{2,}-[A-Z0-9]{2,}', part_str) and not ('φ' in part_str or 'Φ' in part_str):
            # It might be a real part number with a 't' in it (e.g. TRAY-123)
            continue

        # Look for a real part number hiding in the 'role' column
        # Matches typical part numbers like "4F162-001" or "THA-438"
        role_match = re.search(r'([A-Z0-9]+-[A-Z0-9]+)', role_str)
        
        new_note = f"{note_str} / {part_str}".strip(' /')
        
        if role_match:
            new_part_no = role_match.group(1)
            # Remove the part number from role (e.g. "A:5F170-009" -> "A:")
            new_role = role_str.replace(role_match.group(0), '').strip(': ')
            updates.append((new_role, new_part_no, new_note, db_id))
        else:
            # It's a standard role, so there is no part number
            updates.append((role_str, '', new_note, db_id))

    print(f"Found {len(updates)} records to fix.")
    for u in updates[:10]:
        print(f"ID {u[3]}: Role: '{u[0]}', Part: '{u[1]}', Note: '{u[2]}'")

    # Execute updates
    c.executemany('''
        UPDATE bom_components
        SET role = ?, part_no = ?, note = ?
        WHERE id = ?
    ''', updates)

    conn.commit()
    conn.close()
    print("Database updated.")

if __name__ == '__main__':
    fix_dimensions()
