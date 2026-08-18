import glob
import json
import os

files = glob.glob('parsed_bom_*.json')
files.sort(key=os.path.getmtime, reverse=True)

for f in files[:5]:
    try:
        with open(f, encoding='utf-8') as file:
            d = json.load(file)
            filled = sum(1 for i in d if i.get('hinmei') and i.get('hinmei').strip() != "")
            print(f"{f}: {filled} / {len(d)} populated")
            
            # Print one populated example if it exists
            populated = [i for i in d if i.get('hinmei') and i.get('hinmei').strip() != ""]
            if populated:
                print("  Example:", json.dumps(populated[0], ensure_ascii=False))
            else:
                print("  Example: [ALL EMPTY]")
    except Exception as e:
        print(f"Error reading {f}: {e}")
