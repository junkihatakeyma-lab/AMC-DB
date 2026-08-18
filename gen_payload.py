import json

subagents = []
for i in range(50):
    chunks = []
    for j in range(3):
        chunk_num = i * 3 + j
        if chunk_num < 148:
            chunks.append(chunk_num)
    
    if not chunks:
        continue
        
    prompt = f"Please process chunks {', '.join(map(str, chunks))}."
    role = f"Worker {chunks[0]}-{chunks[-1]}"
    
    subagents.append({
        "TypeName": "bom_ocr_worker",
        "Role": role,
        "Prompt": prompt
    })

with open("subagents_payload.json", "w", encoding="utf-8") as f:
    json.dump(subagents, f, ensure_ascii=False, indent=2)

print("Generated subagents_payload.json")
