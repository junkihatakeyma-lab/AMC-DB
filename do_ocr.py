import json
import re
import fitz
import easyocr

def extract_hinmei(text):
    match = re.search(r'品名[\s:：]*([^\n]+)', text)
    if match:
        return match.group(1).strip()
    return "UNKNOWN"

def process_chunk(chunk_num):
    pdf_path = f"chunk_{chunk_num}.pdf"
    json_path = f"chunk_{chunk_num}.json"
    
    with open(json_path, 'r', encoding='utf-8') as f:
        request_nos = json.load(f)
        
    reader = easyocr.Reader(['ja', 'en'], gpu=False)
    results = []
    
    doc = fitz.open(pdf_path)
    for i in range(len(doc)):
        page = doc.load_page(i)
        text = page.get_text()
        hinmei = extract_hinmei(text)
        
        if hinmei == "UNKNOWN":
            pix = page.get_pixmap(dpi=150)
            img_bytes = pix.tobytes("png")
            ocr_results = reader.readtext(img_bytes, detail=0)
            ocr_text = "\n".join(ocr_results)
            hinmei = extract_hinmei(ocr_text)
            
        req_no = request_nos[i] if i < len(request_nos) else f"unknown_{i}"
        
        if not hinmei.startswith("[手書き]"):
            hinmei = "[手書き] " + hinmei
            
        results.append({
            "request_no": req_no,
            "hinmei": hinmei
        })
        if i % 10 == 0:
            print(f"Processed page {i} of chunk {chunk_num}: {hinmei}")
        
    with open(f"parsed_{chunk_num}.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

for n in [47, 48, 49]:
    process_chunk(n)
