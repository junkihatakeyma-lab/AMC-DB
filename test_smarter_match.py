import sqlite3
import collections

conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# 1. Get all mapped BOMs
c.execute("SELECT id, file, new_part_no FROM boms WHERE new_part_no IS NOT NULL")
mapped_boms = c.fetchall()

def get_bom_components(bom_id):
    c.execute("SELECT part_no FROM bom_components WHERE bom_id = ? ORDER BY part_no", (bom_id,))
    return tuple(sorted([row['part_no'] for row in c.fetchall() if row['part_no']]))

boms_by_new_part_no = collections.defaultdict(list)
for bom in mapped_boms:
    boms_by_new_part_no[bom['new_part_no']].append(bom)

passed = 0
unmapped = 0

for new_part_no, boms_list in boms_by_new_part_no.items():
    # Find canonical components
    canonical_comps = None
    
    # Try to find a standard BOM first
    std_boms = [b for b in boms_list if '(#' not in (b['file'] or '') and '（#' not in (b['file'] or '')]
    if std_boms:
        canonical_comps = get_bom_components(std_boms[0]['id'])
    else:
        # If no standard BOM, use the first custom BOM as canonical
        canonical_comps = get_bom_components(boms_list[0]['id'])
        
    for bom in boms_list:
        comps = get_bom_components(bom['id'])
        if comps != canonical_comps:
            unmapped += 1
        else:
            passed += 1

print(f"Passed: {passed}")
print(f"Unmapped: {unmapped}")
