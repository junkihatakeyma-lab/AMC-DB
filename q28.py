import sqlite3

conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute("SELECT id, file FROM boms WHERE new_part_no = 'R0175ASEJU1003U1001045001'")
boms = c.fetchall()

for bom in boms:
    print(f"--- {bom['file']} ---")
    c.execute("SELECT part_no, role, note FROM bom_components WHERE bom_id = ?", (bom['id'],))
    comps = c.fetchall()
    for comp in comps:
        print(f"  {comp['role']}: {comp['part_no']} (Note: {comp['note']})")
