import os
import re
import json

parsed_files = [f for f in os.listdir() if f.startswith('parsed_bom_')]

completed_chunks = set()
for f in parsed_files:
    m = re.search(r'parsed_bom_(\d+)', f)
    if m:
        completed_chunks.add(int(m.group(1)))

missing_chunks = [i for i in range(148) if i not in completed_chunks]
print("Missing chunks count:", len(missing_chunks))

num_workers = 15
subagents = []
chunks_per_worker = len(missing_chunks) // num_workers + (1 if len(missing_chunks) % num_workers != 0 else 0)

for i in range(num_workers):
    start_idx = i * chunks_per_worker
    end_idx = min((i + 1) * chunks_per_worker, len(missing_chunks))
    
    current_batch = missing_chunks[start_idx:end_idx]
    if not current_batch:
        continue
        
    prompt = f"Please process chunks {', '.join(map(str, current_batch))}."
    role = f"Worker {current_batch[0]}-{current_batch[-1]}"
    
    subagents.append({
        "TypeName": "bom_ocr_worker",
        "Role": role,
        "Prompt": prompt
    })

with open("subagents_payload_15.json", "w", encoding="utf-8") as f:
    json.dump(subagents, f, ensure_ascii=False, indent=2)

print(f"Generated subagents_payload_15.json with {len(subagents)} subagents.")
