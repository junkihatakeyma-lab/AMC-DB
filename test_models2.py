import os
import time
from dotenv import load_dotenv
import PIL.Image
from google import genai

load_dotenv()
client = genai.Client()

img_path = r"data/加工依頼書_BOM一体型/#10539.jpg"
img = PIL.Image.open(img_path)

all_models = [m.name for m in client.models.list() if 'gemini' in m.name or 'gemma' in m.name]
working_models = []

for m in all_models:
    print(f"Testing {m}...", flush=True)
    try:
        response = client.models.generate_content(
            model=m,
            contents=["What is this?", img]
        )
        print(f"  SUCCESS! {response.text[:20].encode('ascii', 'ignore').decode()}", flush=True)
        working_models.append(m)
    except Exception as e:
        print(f"  FAILED: {str(e)[:100].encode('ascii', 'ignore').decode()}", flush=True)
    time.sleep(2)

print("\n--- WORKING MODELS ---")
for wm in working_models:
    print(wm)
