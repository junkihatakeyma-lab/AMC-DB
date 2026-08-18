import os
from dotenv import load_dotenv
import PIL.Image
from google import genai

load_dotenv()
client = genai.Client()

img_path = r"data/加工依頼書_BOM一体型/#10539.jpg"
img = PIL.Image.open(img_path)

response = client.models.generate_content(
    model='gemini-1.5-flash',
    contents=["Describe this image", img]
)
print("Success:", response.text)
