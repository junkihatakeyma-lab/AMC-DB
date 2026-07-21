import sys
import json
import re
import easyocr
import fitz  # PyMuPDF
import io
import time
from PIL import Image

def extract_hinmei(text):
    match = re.search(r'品名[\s:：]*([^\n]+)', text)
    if match:
        return match.group(1).strip()
    return ""

def main():
    if len(sys.argv) != 3 or sys.argv[1] != "--chunk":
        print("Usage: python master_ocr.py --chunk <num>")
        sys.exit(1)
        
    chunk_num = sys.argv[2]
    pdf_path = f"chunk_{chunk_num}.pdf"
    json_path = f"chunk_{chunk_num}.json"
    out_path = f"parsed_{chunk_num}.json"
    
    print(f"Processing {pdf_path}...")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        request_nos = json.load(f)
        
    reader = easyocr.Reader(['ja', 'en'], gpu=False) # CPU mode
    
    results = []
    
    doc = fitz.open(pdf_path)
    for i in range(len(doc)):
        page = doc.load_page(i)
        
        # Try text extraction first
        text = page.get_text()
        hinmei = extract_hinmei(text)
        
        # If no text (image-based PDF), use EasyOCR
        if not hinmei:
            pix = page.get_pixmap(dpi=150) # 150 DPI is usually enough for EasyOCR
            img_bytes = pix.tobytes("png")
            
            ocr_results = reader.readtext(img_bytes, detail=0)
            ocr_text = "\n".join(ocr_results)
            
            hinmei = extract_hinmei(ocr_text)
            
        # Ensure we have a request_no
        req_no = request_nos[i] if i < len(request_nos) else f"unknown_{i}"
        
        results.append({
            "request_no": req_no,
            "hinmei": hinmei
        })
        
        # print progress occasionally
        if i % 10 == 0:
            print(f"Chunk {chunk_num}: Processed {i} pages")
            
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    print(f"Finished chunk {chunk_num}. Results saved to {out_path}.")

if __name__ == '__main__':
    main()
