import os
import re

parsed_files = [f for f in os.listdir() if f.startswith('parsed_bom_')]

completed_chunks = set()
for f in parsed_files:
    m = re.search(r'parsed_bom_(\d+)', f)
    if m:
        completed_chunks.add(int(m.group(1)))

print("Completed chunks:", sorted(list(completed_chunks)))
missing_chunks = [i for i in range(148) if i not in completed_chunks]
print("Missing chunks:", missing_chunks)

import json
subagents = []
current_batch = []
worker_count = 0

for chunk in missing_chunks:
    current_batch.append(chunk)
    if len(current_batch) == 3 or chunk == missing_chunks[-1]:
        prompt = f"Please process chunks {', '.join(map(str, current_batch))}."
        role = f"Worker {current_batch[0]}-{current_batch[-1]}"
        subagents.append({
            "TypeName": "bom_ocr_worker",
            "Role": role,
            "Prompt": prompt
        })
        current_batch = []
        worker_count += 1
        
        # Limit to 30 workers at a time to prevent immediate quota exhaustion
        if worker_count >= 30:
            break

with open("subagents_payload_resume.json", "w", encoding="utf-8") as f:
    json.dump(subagents, f, ensure_ascii=False, indent=2)

print(f"Generated subagents_payload_resume.json with {len(subagents)} subagents.")
