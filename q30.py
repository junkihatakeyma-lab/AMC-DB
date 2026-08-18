import json

with open('mapping.json', 'r', encoding='utf-8') as f:
    mapping = json.load(f)

for m in mapping:
    if 'IF100-004-1000' in m['spec'] or 'IF100-004-1000' in m['old_id']:
        print(f"Master: {m['new_id']} - {m['old_id']} - {m['spec']}")
