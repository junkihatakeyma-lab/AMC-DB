import sqlite3

conn = sqlite3.connect('部品DB.sqlite')
c = conn.cursor()

def get_progress(prefix, total_query, params=()):
    c.execute(total_query, params)
    total = c.fetchone()[0]
    
    # We use LIKE for paths because they might have backslashes or forward slashes
    c.execute("SELECT COUNT(DISTINCT file_path) FROM previews WHERE file_path LIKE ? OR file_path LIKE ?", (f'{prefix}%', f'{prefix.replace("/", "\\\\")}%'))
    done = c.fetchone()[0]
    
    return done, total

breakdown = {}

# BOMs
breakdown['BOM'] = get_progress('data/BOM', 'SELECT COUNT(*) FROM boms')

# Requests
breakdown['加工依頼書'] = get_progress('data/加工依頼書', 'SELECT COUNT(*) FROM requests')

# Inspections
breakdown['検査証'] = get_progress('data/検査証', "SELECT COUNT(*) FROM simple_files WHERE type = 'inspection'")

# Photos
breakdown['製品写真'] = get_progress('data/製品写真', "SELECT COUNT(*) FROM simple_files WHERE type = 'photo'")

# Drawings
breakdown['図面'] = get_progress('data/図面', "SELECT COUNT(*) FROM simple_files WHERE type = 'drawing'")

for name, (done, total) in breakdown.items():
    print(f"{name}: Done {done} / Total {total}")
