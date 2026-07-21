import json

with open('chunk_8.json', encoding='utf-8') as f:
    data = json.load(f)

with open('dump.txt', 'w', encoding='utf-8') as f:
    for i, d in enumerate(data):
        f.write(f'--- {i} {d["file"]} ---\n')
        f.write(d['text'].strip() + '\n\n')
