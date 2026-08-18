import os
import json
import PIL.Image
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()

with open('bom_chunk_133.json', 'r', encoding='utf-8') as f:
    paths = json.load(f)[:10]

contents = ["What are the part numbers?"]
for p in paths:
    img = PIL.Image.open(p)
    img.thumbnail((1024, 1024))
    contents.append(img)

print("Sending request...")
response = client.models.generate_content(
    model='gemini-3.1-flash-lite-preview',
    contents=contents,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
    )
)
print("Response:", response.text)
