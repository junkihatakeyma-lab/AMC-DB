import sqlite3

conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
c = conn.cursor()

# 1. BOMs
c.execute("SELECT COUNT(*) FROM boms")
total_boms = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM boms WHERE new_part_no IS NOT NULL")
mapped_boms = c.fetchone()[0]

# 2. Requests
c.execute("SELECT COUNT(*) FROM requests")
total_reqs = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM requests WHERE new_part_no IS NOT NULL")
mapped_reqs = c.fetchone()[0]

# 3. Drawings (simple_files type='drawing')
c.execute("SELECT COUNT(*) FROM simple_files WHERE type='drawing'")
total_drawings = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM simple_files WHERE type='drawing' AND length(link_key) = 25")
mapped_drawings = c.fetchone()[0]

conn.close()

def pct(part, total):
    if total == 0: return 0.0
    return (part / total) * 100

print(f"BOMs: {mapped_boms} / {total_boms} ({pct(mapped_boms, total_boms):.1f}%)")
print(f"Requests: {mapped_reqs} / {total_reqs} ({pct(mapped_reqs, total_reqs):.1f}%)")
print(f"Drawings: {mapped_drawings} / {total_drawings} ({pct(mapped_drawings, total_drawings):.1f}%)")

total_all = total_boms + total_reqs + total_drawings
mapped_all = mapped_boms + mapped_reqs + mapped_drawings
print(f"Overall: {mapped_all} / {total_all} ({pct(mapped_all, total_all):.1f}%)")
