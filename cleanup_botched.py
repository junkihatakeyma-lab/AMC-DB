import glob
import json
import os
import codecs

files = glob.glob('parsed_bom_*.json')
deleted = 0

def load_json(f):
    encodings = ['utf-8', 'utf-8-sig', 'shift_jis', 'utf-16']
    for enc in encodings:
        try:
            with open(f, 'r', encoding=enc) as file:
                return json.load(file)
        except Exception:
            continue
    return None

for f in files:
    data = load_json(f)
    if data is None:
        print(f"Could not load {f}, it might be empty or corrupt. Deleting.")
        try:
            os.remove(f)
            deleted += 1
        except:
            pass
        continue

    empty_count = sum(1 for item in data if not item.get("hinmei"))
    if len(data) == 0 or empty_count / len(data) > 0.5:
        print(f"Deleting {f} (empty or mostly empty)")
        os.remove(f)
        deleted += 1

print(f"Deleted {deleted} botched files.")
