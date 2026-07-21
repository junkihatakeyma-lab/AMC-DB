import os
import json
import re
import easyocr
import fitz  # PyMuPDF
import concurrent.futures
import time
import multiprocessing

def extract_hinmei(text):
    match = re.search(r'品名[\s:：]*([^\n]+)', text)
    if match:
        return match.group(1).strip()
    return ""

def process_chunk(chunk_num):
    pdf_path = f"chunk_{chunk_num}.pdf"
    json_path = f"chunk_{chunk_num}.json"
    out_path = f"parsed_{chunk_num}.json"
    
    if os.path.exists(out_path):
        print(f"Chunk {chunk_num} already processed. Skipping.")
        return
        
    if not os.path.exists(pdf_path):
        print(f"Chunk {chunk_num} PDF not found. Skipping.")
        return

    print(f"Processing chunk {chunk_num}...")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        request_nos = json.load(f)
        
    # Each process loads EasyOCR once
    reader = easyocr.Reader(['ja', 'en'], gpu=False) 
    
    results = []
    try:
        doc = fitz.open(pdf_path)
        for i in range(len(doc)):
            page = doc.load_page(i)
            text = page.get_text()
            hinmei = extract_hinmei(text)
            
            if not hinmei:
                pix = page.get_pixmap(dpi=150)
                img_bytes = pix.tobytes("png")
                ocr_results = reader.readtext(img_bytes, detail=0)
                ocr_text = "\n".join(ocr_results)
                hinmei = extract_hinmei(ocr_text)
                
            req_no = request_nos[i] if i < len(request_nos) else f"unknown_{i}"
            results.append({"request_no": req_no, "hinmei": hinmei})
            
            if i > 0 and i % 50 == 0:
                print(f"Chunk {chunk_num}: Processed {i} pages")
                
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
        print(f"Finished chunk {chunk_num}. Total items: {len(results)}")
    except Exception as e:
        print(f"Error processing chunk {chunk_num}: {e}")

def main():
    print("Starting multiprocessing OCR for chunks 0-49...")
    start_time = time.time()
    
    # We use 2 workers to avoid Out of Memory (OOM) errors with EasyOCR
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        # Wrap in list() to actually consume the generator and raise any exceptions
        try:
            list(executor.map(process_chunk, range(50)))
        except Exception as e:
            print(f"Fatal error in multiprocessing: {e}")
        
    print(f"All chunks completed in {time.time()-start_time:.1f}s!")

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
