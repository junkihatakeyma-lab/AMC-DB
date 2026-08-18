import glob
import re
import os

parsed_files = glob.glob('parsed_bom_*.json')
print("Total parsed files:", len(parsed_files))

chunks = set()
for f in parsed_files:
    m = re.search(r'parsed_bom_(\d+)', f)
    if m:
        chunks.add(int(m.group(1)))

completed = sorted(list(chunks))
print("Completed chunks:", completed)

missing = [i for i in range(148) if i not in completed]
print("Missing chunks count:", len(missing))
