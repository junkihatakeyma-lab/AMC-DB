import sqlite3
import os
from PIL import Image

def make_pdf():
    conn = sqlite3.connect('部品DB.sqlite')
    c = conn.cursor()
    # Get 10 unprocessed handwritten files
    rows = c.execute("SELECT request_no, file FROM requests WHERE is_handwritten=1 AND hinmei='' LIMIT 10").fetchall()
    
    images = []
    for row in rows:
        req_no, fpath = row
        if os.path.exists(fpath):
            try:
                img = Image.open(fpath).convert('RGB')
                images.append(img)
            except Exception as e:
                print(f"Error opening {fpath}: {e}")
                
    if images:
        images[0].save('test_batch.pdf', save_all=True, append_images=images[1:])
        print(f"Saved {len(images)} images to test_batch.pdf")
    else:
        print("No images found.")

if __name__ == "__main__":
    make_pdf()
