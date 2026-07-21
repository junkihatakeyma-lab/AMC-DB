import json

with open('chunk_1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('chunk_1_readable.txt', 'w', encoding='utf-8') as f:
    for item in data:
        f.write(f"--- FILE: {item['file']} ---\n")
        f.write(item['text'])
        f.write("\n\n")
