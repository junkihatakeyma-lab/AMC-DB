import os
import re
import json

def cleanup():
    files = [f for f in os.listdir() if f.startswith('parsed_bom_')]
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                data = json.load(file)
            empty_count = sum(1 for item in data if not item.get("hinmei"))
            if len(data) > 0 and empty_count / len(data) > 0.5:
                os.remove(f)
        except Exception:
            try:
                os.remove(f)
            except:
                pass

def get_missing_chunks():
    files = [f for f in os.listdir() if f.startswith('parsed_bom_')]
    completed = set()
    for f in files:
        m = re.search(r'parsed_bom_(\d+)', f)
        if m:
            completed.add(int(m.group(1)))
    return [i for i in range(148) if i not in completed]

cleanup()
missing = get_missing_chunks()
print(f"Missing chunks count: {len(missing)}")

if not missing:
    print("ALL DONE")
else:
    # We want to process exactly 15 chunks, 1 chunk per subagent
    batch = missing[:15]
    subagents = []
    for chunk in batch:
        subagents.append({
            "TypeName": "bom_ocr_worker",
            "Role": f"Worker {chunk}",
            "Prompt": f"Please process chunk {chunk}."
        })
    with open("next_batch_payload.json", "w", encoding="utf-8") as f:
        json.dump(subagents, f, ensure_ascii=False, indent=2)
    print("Generated next_batch_payload.json")
