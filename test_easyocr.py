import easyocr
import sys
import os

def test():
    print("Loading EasyOCR model...")
    # Hide progress bars from stderr by temporarily redirecting it
    old_stderr = sys.stderr
    with open('easyocr_download.log', 'w') as f:
        sys.stderr = f
        try:
            reader = easyocr.Reader(['ja', 'en'])
        finally:
            sys.stderr = old_stderr
            
    print("Model loaded. Testing images...")
    
    files = [
        'data/加工依頼書_自動読取/#001.jpg',
        'data/加工依頼書_自動読取/#002.jpg',
        'data/加工依頼書_自動読取/#003.jpg',
        'data/加工依頼書_自動読取/#004.jpg',
        'data/加工依頼書_自動読取/#005.jpg'
    ]
    
    results = []
    for f in files:
        if os.path.exists(f):
            print(f"Reading {f}...")
            res = reader.readtext(f, detail=0)
            text = " ".join(res)
            results.append({"file": f, "extracted": text})
            print(f"  Result: {text}")
        else:
            print(f"File not found: {f}")

if __name__ == "__main__":
    test()
