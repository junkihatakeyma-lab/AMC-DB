import json
import sqlite3
import os
import glob

def update_db():
    conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
    c = conn.cursor()
    
    count = 0
    files = glob.glob('parsed_*.json')
    print(f"Found {len(files)} parsed files.")
    
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                
                # If data is a dict (from older format), extract the list of items
                if isinstance(data, dict):
                    # In older format, data is a dict where keys are filenames and values are lists of objects
                    items = []
                    for k, v in data.items():
                        if isinstance(v, list):
                            items.extend(v)
                else:
                    items = data
                    
                for item in items:
                    if not isinstance(item, dict): continue
                    req_no = item.get('request_no')
                    hinmei = item.get('hinmei', '').strip()
                    
                    if hinmei:
                        # Append [手書き] prefix to clearly indicate it was OCR'd
                        if not hinmei.startswith('[手書き]'):
                            hinmei = f"[手書き] {hinmei}"
                            
                        c.execute("UPDATE requests SET hinmei = ? WHERE request_no = ?", (hinmei, req_no))
                        count += c.rowcount
            except json.JSONDecodeError:
                print(f"Error reading {file_path}")
                
    conn.commit()
    conn.close()
    print(f"Updated {count} items in the database.")

if __name__ == "__main__":
    update_db()
