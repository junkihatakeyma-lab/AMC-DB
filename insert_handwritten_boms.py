import json
import sqlite3
import os
import glob
import re

DB_PATH = '部品DB.sqlite'

def clean_request_no(req_no):
    if not req_no:
        return ""
    req_no = str(req_no).strip()
    if req_no.startswith('#') or req_no.startswith('＃'):
        req_no = req_no[1:]
    return req_no

def insert_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    files = glob.glob('parsed_bom_*.json')
    print(f"Found {len(files)} JSON files.")
    
    # Check if a BOM already exists for a request to prevent duplicates
    c.execute("SELECT request_no FROM bom_requests")
    existing_requests = set(row[0] for row in c.fetchall())
    
    total_boms = 0
    total_components = 0
    
    for file_path in files:
        print(f"Processing {file_path}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            for item in data:
                req_no = clean_request_no(item.get('request_no'))
                if not req_no:
                    continue
                    
                hinmei = item.get('hinmei', '').strip()
                components = item.get('components', [])
                
                # 1. Update requests.hinmei
                if hinmei:
                    if not hinmei.startswith('[手書き]'):
                        hinmei = f"[手書き] {hinmei}"
                    c.execute("UPDATE requests SET hinmei = ? WHERE request_no = ?", (hinmei, req_no))
                
                # 2. Insert BOM and components if not already processed
                if req_no not in existing_requests and components:
                    # Create dummy BOM
                    c.execute("INSERT INTO boms (product_code, seiban, layout_ok) VALUES ('', '', 0)")
                    bom_id = c.lastrowid
                    
                    # Link to request
                    c.execute("INSERT INTO bom_requests (bom_id, request_no) VALUES (?, ?)", (bom_id, req_no))
                    
                    # Insert components
                    for comp in components:
                        if isinstance(comp, dict):
                            part_no = str(comp.get('part_no', '')).strip()
                        elif isinstance(comp, str):
                            part_no = comp.strip()
                        else:
                            continue
                            
                        if part_no:
                            c.execute("INSERT INTO bom_components (bom_id, role, part_no, note) VALUES (?, '', ?, '')", (bom_id, part_no))
                            total_components += 1
                            
                    existing_requests.add(req_no)
                    total_boms += 1
                    
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            
    conn.commit()
    conn.close()
    print(f"Done! Created {total_boms} BOMs and {total_components} components.")

if __name__ == "__main__":
    insert_data()
