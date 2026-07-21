import json
import sqlite3
import re
import os

def collect_from_transcript():
    transcript_path = r"C:\Users\jhatakeyama\.gemini\antigravity\brain\5aaa5b37-386d-4d71-9197-21c196671aa6\.system_generated\logs\transcript_full.jsonl"
    
    if not os.path.exists(transcript_path):
        print("Transcript not found")
        return
        
    extracted_data = []
    
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line)
                content = entry.get('content', '')
                if '```python' in content and 'data =' in content:
                    # Extract the data array
                    match = re.search(r'data\s*=\s*(\[.*?\])\s*with open', content, re.DOTALL)
                    if match:
                        json_str = match.group(1)
                        # Fix any potential python-specific things to make it valid JSON
                        json_str = json_str.replace("'", '"')
                        data = json.loads(json_str)
                        extracted_data.extend(data)
            except Exception as e:
                pass
                
    if extracted_data:
        conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
        c = conn.cursor()
        count = 0
        for item in extracted_data:
            c.execute("UPDATE requests SET hinmei = ? WHERE request_no = ?", (item['hinmei'], item['request_no']))
            count += 1
        conn.commit()
        print(f"Updated {count} items in the database from transcript.")
    else:
        print("No data found yet.")

if __name__ == "__main__":
    collect_from_transcript()
