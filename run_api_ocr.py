import os
import json
import re
import time
import glob
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
import PIL.Image

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")
client = genai.Client()

def get_missing_chunks():
    parsed_files = glob.glob('parsed_bom_*.json')
    completed = set()
    for f in parsed_files:
        m = re.search(r'parsed_bom_(\d+)', f)
        if m:
            completed.add(int(m.group(1)))
    return [i for i in range(148) if i not in completed]

def process_batch(images_data, retries=3):
    prompt = f"""You are an expert OCR assistant.
I will provide you with {len(images_data)} images of manufacturing processing requests (加工依頼書).
Please extract the handwritten 'hinmei' (item name) and 'components' (part numbers) from each image.

Here are the request numbers corresponding to the {len(images_data)} images in the exact order they are attached:
"""
    for i, data in enumerate(images_data):
        prompt += f"Image {i+1}: request_no = '{data['request_no']}'\n"

    prompt += """
Please output a JSON array of objects, exactly one object for each image in the exact order.
Example format:
[
  {
    "request_no": "123",
    "hinmei": "[手書き] IF104-0600",
    "components": [
      {"part_no": "IF104-401-0600"},
      {"part_no": "E-616"}
    ]
  }
]

Rules:
1. If there are no handwritten notes/BOM for an image, set 'hinmei' to "" and 'components' to [].
2. ONLY output a raw JSON array. Do not include markdown code blocks like ```json ... ```.
3. Be as accurate as possible in reading handwritten alphanumeric characters.
"""

    contents = [prompt]
    for data in images_data:
        try:
            img = PIL.Image.open(data['path'])
            img.thumbnail((1024, 1024))
            contents.append(img)
        except Exception as e:
            print(f"Error loading image {data['path']}: {e}")
            contents.append(f"[Image {data['request_no']} failed to load]")

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model='gemini-3.1-flash-lite-preview',
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                )
            )
            raw_text = response.text
            parsed = json.loads(raw_text)
            
            if len(parsed) != len(images_data):
                print(f"Warning: Model returned {len(parsed)} items, expected {len(images_data)}.")
                
            return parsed
        except Exception as e:
            safe_error = str(e).encode('cp932', errors='replace').decode('cp932')
            print(f"Attempt {attempt+1} failed: {safe_error}")
            time.sleep(10 * (attempt + 1))
            
    print("Failed after all retries. Aborting script to avoid writing empty data.")
    os._exit(1)

def main():
    missing_chunks = get_missing_chunks()
    print(f"Found {len(missing_chunks)} missing chunks to process.")
    
    for chunk_idx in missing_chunks:
        print(f"=== Processing chunk {chunk_idx} ===")
        chunk_file = f"bom_chunk_{chunk_idx}.json"
        
        if not os.path.exists(chunk_file):
            continue
            
        with open(chunk_file, 'r', encoding='utf-8') as f:
            chunk_data = json.load(f)
            
        images_info = []
        for path in chunk_data:
            basename = os.path.basename(path)
            request_no = os.path.splitext(basename)[0]
            images_info.append({"request_no": request_no, "path": path})
            
        BATCH_SIZE = 10
        all_results = []
        
        for i in range(0, len(images_info), BATCH_SIZE):
            batch = images_info[i:i+BATCH_SIZE]
            print(f"  -> Batch {i//BATCH_SIZE + 1} ({len(batch)} images)", flush=True)
            
            results = process_batch(batch)
            if results:
                all_results.extend(results)
                
            time.sleep(4)
            
        output_file = f"parsed_bom_{chunk_idx}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        print(f"Saved {output_file} with {len(all_results)} records.", flush=True)

if __name__ == "__main__":
    main()
