import sqlite3
import os

DB_PATH = "部品DB.sqlite"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    # 1. products (製品マスター)
    c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_code TEXT PRIMARY KEY,
        name TEXT,
        alias TEXT
    )
    ''')

    # 2. seibans (製番管理)
    c.execute('''
    CREATE TABLE IF NOT EXISTS seibans (
        seiban TEXT PRIMARY KEY,
        product_code TEXT,
        request_no TEXT
    )
    ''')

    # 3. requests (加工依頼書)
    c.execute('''
    CREATE TABLE IF NOT EXISTS requests (
        request_no TEXT PRIMARY KEY,
        issue_date TEXT,
        hinmei TEXT,
        qty TEXT,
        kiji TEXT,
        yoto TEXT,
        noki_raw TEXT,
        noki TEXT,
        dest TEXT,
        spec TEXT,
        biko TEXT,
        prev TEXT,
        seiban TEXT,
        file TEXT
    )
    ''')

    # 4. boms (部品構成表)
    c.execute('''
    CREATE TABLE IF NOT EXISTS boms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_code TEXT,
        seiban TEXT,
        layout_ok BOOLEAN,
        file TEXT UNIQUE
    )
    ''')

    # 5. bom_components (BOM内の各部品)
    c.execute('''
    CREATE TABLE IF NOT EXISTS bom_components (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bom_id INTEGER,
        role TEXT,
        part_no TEXT,
        note TEXT,
        FOREIGN KEY(bom_id) REFERENCES boms(id) ON DELETE CASCADE
    )
    ''')

    # 6. bom_requests (BOMと関連依頼書の紐付け)
    c.execute('''
    CREATE TABLE IF NOT EXISTS bom_requests (
        bom_id INTEGER,
        request_no TEXT,
        FOREIGN KEY(bom_id) REFERENCES boms(id) ON DELETE CASCADE
    )
    ''')

    # 7. inspections / photos (検査証・写真)
    c.execute('''
    CREATE TABLE IF NOT EXISTS simple_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT, -- 'inspection', 'photo', or 'drawing'
        file_path TEXT,
        link_key TEXT -- 品番 / 製番 / 依頼No のいずれか
    )
    ''')

    # 8. previews (各ファイルのプレビュー画像)
    c.execute('''
    CREATE TABLE IF NOT EXISTS previews (
        file_path TEXT,
        preview_path TEXT,
        page_num INTEGER
    )
    ''')

    # 9. files (ファイルの差分管理用)
    c.execute('''
    CREATE TABLE IF NOT EXISTS files (
        file_path TEXT PRIMARY KEY,
        mtime REAL,
        hash TEXT
    )
    ''')

    # 10. exceptions (AI例外処理用)
    c.execute('''
    CREATE TABLE IF NOT EXISTS exceptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_path TEXT UNIQUE,
        raw_text TEXT,
        parsed_json TEXT,
        status TEXT -- 'pending', 'confirmed'
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
