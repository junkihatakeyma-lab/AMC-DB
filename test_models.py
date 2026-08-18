import os
import time
from dotenv import load_dotenv
import PIL.Image
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()

img_path = r"data/加工依頼書_BOM一体型/#10539.jpg"
img = PIL.Image.open(img_path)

models_to_test = [
    'gemini-3.5-flash-lite',
    'gemini-flash-lite-latest',
    'gemini-3.1-flash-lite',
    'gemini-3.6-flash'
]

for m in models_to_test:
    print(f"Testing {m}...")
    try:
        response = client.models.generate_content(
            model=m,
            contents=["What is this?", img]
        )
        print(f"  SUCCESS! {response.text[:20]}")
    except Exception as e:
        print(f"  FAILED: {e}")
    time.sleep(2)
