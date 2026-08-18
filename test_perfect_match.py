import sqlite3
import collections

conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# 1. Get all mapped BOMs
c.execute("SELECT id, file, new_part_no FROM boms WHERE new_part_no IS NOT NULL")
boms = c.fetchall()

# 2. Build standard BOMs dictionary
standard_boms = collections.defaultdict(list)
custom_boms = []

for bom in boms:
    if '(#' in bom['file'] or '（#' in bom['file']:
        custom_boms.append(bom)
    else:
        standard_boms[bom['new_part_no']].append(bom)

def get_bom_components(bom_id):
    c.execute("SELECT part_no FROM bom_components WHERE bom_id = ? ORDER BY part_no", (bom_id,))
    return tuple(sorted([row['part_no'] for row in c.fetchall() if row['part_no']]))

# 3. Cache standard components
standard_components = {}
for new_part_no, std_list in standard_boms.items():
    # We just take the first standard BOM's components as the "truth"
    if std_list:
        standard_components[new_part_no] = get_bom_components(std_list[0]['id'])

# 4. Check custom BOMs
passed = 0
failed_no_standard = 0
failed_mismatch = 0

for bom in custom_boms:
    new_part_no = bom['new_part_no']
    
    if new_part_no not in standard_components:
        failed_no_standard += 1
        continue
        
    custom_comps = get_bom_components(bom['id'])
    std_comps = standard_components[new_part_no]
    
    if custom_comps == std_comps:
        passed += 1
    else:
        failed_mismatch += 1

print(f"Total custom BOMs: {len(custom_boms)}")
print(f"Passed (perfect match): {passed}")
print(f"Failed (no standard BOM exists): {failed_no_standard}")
print(f"Failed (component mismatch): {failed_mismatch}")
