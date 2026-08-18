import os
import json
from dotenv import load_dotenv
import PIL.Image
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()

img_path = r"data/加工依頼書_BOM一体型/#10539.jpg"
img = PIL.Image.open(img_path)

prompt = """You are an expert OCR assistant.
Please extract the handwritten 'hinmei' (item name) and 'components' (part numbers) from this image.
The request number for this image is '10539'.

Please output a JSON array of objects, exactly one object for this image.
Example format:
[
  {
    "request_no": "10539",
    "hinmei": "[手書き] IF104-0600",
    "components": [
      {"part_no": "IF104-401-0600"},
      {"part_no": "E-616"}
    ]
  }
]
"""

response = client.models.generate_content(
    model='gemini-3.5-flash-lite',
    contents=[prompt, img],
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
    )
)
print(response.text)
