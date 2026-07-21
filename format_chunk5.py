import json

with open("C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/chunk_5.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/chunk_5_readable.txt", "w", encoding="utf-8") as out:
    for item in data:
        out.write(f"FILE_START: {item['file']}\n")
        out.write(item["text"] + "\n")
        out.write("FILE_END\n\n")
