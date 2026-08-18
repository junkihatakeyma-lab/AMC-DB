import os
import re

parsed_files = [f for f in os.listdir() if f.startswith('parsed_bom_')]

completed_chunks = set()
for f in parsed_files:
    m = re.search(r'parsed_bom_(\d+)', f)
    if m:
        completed_chunks.add(int(m.group(1)))

missing_chunks = [i for i in range(148) if i not in completed_chunks]
import json

with open("subagents_payload_resume.json", "r", encoding="utf-8") as f:
    launched = json.load(f)

launched_chunks = set()
for item in launched:
    prompt = item["Prompt"]
    m = re.findall(r'\d+', prompt)
    for c in m:
        launched_chunks.add(int(c))

still_missing = [c for c in missing_chunks if c not in launched_chunks]

subagents = []
current_batch = []
for chunk in still_missing:
    current_batch.append(chunk)
    if len(current_batch) == 3 or chunk == still_missing[-1]:
        prompt = f"Please process chunks {', '.join(map(str, current_batch))}."
        role = f"Worker {current_batch[0]}-{current_batch[-1]}"
        subagents.append({
            "TypeName": "bom_ocr_worker",
            "Role": role,
            "Prompt": prompt
        })
        current_batch = []

with open("subagents_payload_final.json", "w", encoding="utf-8") as f:
    json.dump(subagents, f, ensure_ascii=False, indent=2)

print(f"Generated subagents_payload_final.json with {len(subagents)} subagents.")
