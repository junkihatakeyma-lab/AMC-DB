import os
import sqlite3

DB_PATH = '部品DB.sqlite'
INPUT_DIR = r'data\加工依頼書_自動読取'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    return conn, c

def main():
    if not os.path.exists(INPUT_DIR):
        print(f"Directory {INPUT_DIR} does not exist.")
        return

    conn, c = init_db()
    
    files = os.listdir(INPUT_DIR)
    if not files:
        print(f"No files found in {INPUT_DIR}")
        return
        
    success_count = 0
    for filename in files:
        file_path = os.path.join(INPUT_DIR, filename)
        if not os.path.isfile(file_path):
            continue
            
        ext = os.path.splitext(filename)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png']:
            continue
            
        # Strip "#" or "＃" from start
        base_name = os.path.splitext(filename)[0]
        if base_name.startswith('#') or base_name.startswith('＃'):
            request_no = base_name[1:]
        else:
            request_no = base_name
            
        db_path = file_path.replace('\\', '/')
        
        # Check if already imported by exact file path
        c.execute("SELECT 1 FROM requests WHERE file = ?", (db_path,))
        if c.fetchone():
            continue
            
        # Check if request_no already exists
        c.execute("SELECT 1 FROM requests WHERE request_no = ?", (request_no,))
        if c.fetchone():
            print(f"Warning: request_no {request_no} already exists in DB. Skipping to prevent overwrite.")
            continue
            
        try:
            c.execute("""
                INSERT INTO requests (request_no, seiban, hinmei, biko, file, issue_date, qty, kiji, yoto, noki_raw, noki, dest, spec, prev, is_handwritten)
                VALUES (?, ?, ?, ?, ?, '', '', '', '', '', '', '', '', '', 1)
            """, (request_no, '', '', '', db_path))
            
            success_count += 1
            if success_count % 1000 == 0:
                print(f"Inserted {success_count} files...")
                conn.commit()
        except Exception as e:
            print(f"Database error for {filename}: {e}")

    conn.commit()
    print(f"\nDone! Successfully processed and saved {success_count} files.")
    conn.close()

if __name__ == "__main__":
    main()
