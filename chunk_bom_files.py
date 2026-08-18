import os
import json
import glob

files = glob.glob('data/加工依頼書_BOM一体型/*.jpg')
# Sort by filename logically
files.sort(key=lambda x: os.path.basename(x))

chunk_size = 100
for i in range(0, len(files), chunk_size):
    chunk = files[i:i + chunk_size]
    chunk_index = i // chunk_size
    with open(f'bom_chunk_{chunk_index}.json', 'w', encoding='utf-8') as f:
        json.dump(chunk, f, ensure_ascii=False, indent=2)

print(f"Created {len(files) // chunk_size + (1 if len(files) % chunk_size != 0 else 0)} chunks for {len(files)} files.")
