import os
import json
import sqlite3

def collect():
    conn = sqlite3.connect('部品DB.sqlite')
    c = conn.cursor()
    
    total_updated = 0
    for i in range(10):
        fname = f'parsed_{i}.json'
        if os.path.exists(fname):
            try:
                with open(fname, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for item in data:
                    c.execute("UPDATE requests SET hinmei = ? WHERE request_no = ?", (item.get('hinmei', ''), item.get('request_no')))
                    total_updated += 1
                os.remove(fname)
                os.remove(f'chunk_{i}.pdf')
                os.remove(f'chunk_{i}.json')
            except Exception as e:
                print(f"Error processing {fname}: {e}")
                
    conn.commit()
    print(f"Updated {total_updated} items in the database.")
    
if __name__ == "__main__":
    collect()
