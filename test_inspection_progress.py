import sqlite3

conn = sqlite3.connect('部品DB.sqlite')
c = conn.cursor()

# Total inspection certificates
c.execute("SELECT COUNT(*) FROM simple_files WHERE type = 'inspection'")
total_inspections = c.fetchone()[0]

# Inspection certificates with previews generated
c.execute("SELECT COUNT(DISTINCT file_path) FROM previews WHERE file_path LIKE 'data/検査証%' OR file_path LIKE 'data\\検査証%'")
done_inspections = c.fetchone()[0]

print(f"Done: {done_inspections} / Total: {total_inspections}")
