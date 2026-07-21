import sqlite3
import os
import json
from PIL import Image

def make_chunks():
    conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
    c = conn.cursor()
    # Get 5000 unprocessed handwritten files
    rows = c.execute("SELECT request_no, file FROM requests WHERE is_handwritten=1 AND hinmei='' LIMIT 5000").fetchall()
    
    if not rows:
        print("No more unprocessed handwritten requests found.")
        return

    chunk_size = 100
    chunks = [rows[i:i+chunk_size] for i in range(0, len(rows), chunk_size)]
    
    for i, chunk in enumerate(chunks):
        images = []
        mapping = []
        for req_no, fpath in chunk:
            if os.path.exists(fpath):
                try:
                    img = Image.open(fpath).convert('RGB')
                    images.append(img)
                    mapping.append(req_no)
                except Exception as e:
                    print(f"Error opening {fpath}: {e}")
                    
        if images:
            pdf_path = f'chunk_{i}.pdf'
            json_path = f'chunk_{i}.json'
            
            images[0].save(pdf_path, save_all=True, append_images=images[1:])
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(mapping, f, ensure_ascii=False, indent=2)
                
            print(f"Created {pdf_path} and {json_path} with {len(images)} items.")

if __name__ == "__main__":
    make_chunks()
