import sqlite3
import pandas as pd
import re
import os
import json

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    firebase_admin = None

DB_PATH = "部品DB.sqlite"
MASTER_EXCEL_PATH = "data/部品マスタ/部品マスタ.xlsx"
MANUAL_LINK_EXCEL_PATH = "data/部品マスタ/手動紐付け用.xlsx"

import unicodedata

def normalize(text):
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize('NFKC', text)
    text = text.upper()
    text = re.sub(r'[^A-Z0-9]', '', text)
    return text

def init_master_tables(conn):
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS parts_master (
        master_id TEXT PRIMARY KEY,
        hinmei TEXT,
        kbn TEXT,
        k_sunpo TEXT,
        zaishitsu TEXT,
        tani TEXT
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS part_master_links (
        db_part_no TEXT PRIMARY KEY,
        master_id TEXT,
        match_type TEXT
    )
    ''')
    c.execute("DELETE FROM parts_master")
    c.execute("DELETE FROM part_master_links")
    conn.commit()

def import_master_data(conn):
    print(f"Loading master data from {MASTER_EXCEL_PATH} ...")
    df = pd.read_excel(MASTER_EXCEL_PATH)
    
    # Fill NaN with empty string
    df = df.fillna("")
    
    c = conn.cursor()
    inserted_count = 0
    
    # Identify required columns based on previous investigation
    col_id = "品番・図番"
    col_name = "品名"
    col_kbn = "品番区分"
    col_sunpo = "形式・寸法"
    col_zai = "材質"
    col_tani = "単位"
    
    for _, row in df.iterrows():
        m_id = str(row.get(col_id, "")).strip()
        if not m_id:
            continue
            
        try:
            c.execute('''
                INSERT OR REPLACE INTO parts_master (master_id, hinmei, kbn, k_sunpo, zaishitsu, tani)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                m_id, 
                str(row.get(col_name, "")), 
                str(row.get(col_kbn, "")), 
                str(row.get(col_sunpo, "")), 
                str(row.get(col_zai, "")), 
                str(row.get(col_tani, ""))
            ))
            inserted_count += 1
        except Exception as e:
            print(f"Error inserting {m_id}: {e}")
            
    conn.commit()
    print(f"Imported {inserted_count} master records.")

def generate_links(conn):
    c = conn.cursor()
    
    # 1. Fetch DB Parts
    c.execute("SELECT DISTINCT part_no FROM bom_components WHERE part_no IS NOT NULL AND part_no != ''")
    bom_parts = [r[0] for r in c.fetchall()]
    
    c.execute("SELECT DISTINCT link_key FROM simple_files WHERE link_key IS NOT NULL AND link_key != ''")
    simple_parts = [r[0] for r in c.fetchall()]
    
    all_db_parts = list(set(bom_parts + simple_parts))
    print(f"Found {len(all_db_parts)} unique parts in Database.")
    
    # 2. Fetch Master Parts
    c.execute("SELECT master_id FROM parts_master")
    master_parts = [r[0] for r in c.fetchall()]
    norm_master = {normalize(p): p for p in master_parts if normalize(p)}
    
    links_to_insert = []
    linked_db_parts = set()
    
    # 3. Process Manual Links if exist
    manual_count = 0
    if os.path.exists(MANUAL_LINK_EXCEL_PATH):
        print(f"Loading manual links from {MANUAL_LINK_EXCEL_PATH} ...")
        df_manual = pd.read_excel(MANUAL_LINK_EXCEL_PATH)
        for _, row in df_manual.iterrows():
            db_id = str(row.iloc[0]).strip()
            m_id = str(row.iloc[1]).strip()
            if db_id and m_id:
                # verify master_id exists
                if m_id in master_parts:
                    links_to_insert.append((db_id, m_id, 'manual_excel'))
                    linked_db_parts.add(db_id)
                    manual_count += 1
                else:
                    print(f"Warning: Manual link master_id '{m_id}' not found in Parts Master.")
                    
    # 3.5 Fetch Manual Links from Firestore
    if firebase_admin and os.path.exists("serviceAccountKey.json"):
        print("Fetching manual links from Firestore...")
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate("serviceAccountKey.json")
                firebase_admin.initialize_app(cred)
            db = firestore.client()
            docs = db.collection("manual_part_links").stream()
            for doc in docs:
                data = doc.to_dict()
                db_id = str(data.get("db_part_no", "")).strip()
                m_id = str(data.get("master_id", "")).strip()
                if db_id and m_id and db_id not in linked_db_parts:
                    if m_id in master_parts:
                        links_to_insert.append((db_id, m_id, 'manual_firestore'))
                        linked_db_parts.add(db_id)
                        manual_count += 1
                    else:
                        print(f"Warning: Firestore manual link master_id '{m_id}' not found in Parts Master.")
        except Exception as e:
            print(f"Error fetching from Firestore: {e}")
    else:
        print("Skipping Firestore sync (serviceAccountKey.json not found or firebase-admin not installed).")
    
    # 4. Fuzzy Match for remaining parts
    print("Performing fuzzy matching for remaining parts...")
    fuzzy_match_count = 0
    for db_p in all_db_parts:
        if db_p in linked_db_parts:
            continue
            
        norm_db = normalize(db_p)
        if not norm_db:
            continue
            
        matched_m_id = None
        
        # Exact match on normalized
        if norm_db in norm_master:
            matched_m_id = norm_master[norm_db]
        # Substring match (Master contains DB)
        elif len(norm_db) >= 5:
            for m_norm, m_orig in norm_master.items():
                if norm_db in m_norm:
                    matched_m_id = m_orig
                    break
                    
        if matched_m_id:
            links_to_insert.append((db_p, matched_m_id, 'auto'))
            linked_db_parts.add(db_p)
            fuzzy_match_count += 1
            
    # Insert links
    c.executemany("INSERT OR REPLACE INTO part_master_links (db_part_no, master_id, match_type) VALUES (?, ?, ?)", links_to_insert)
    conn.commit()
    print(f"Generated {len(links_to_insert)} links (Manual: {manual_count}, Auto: {fuzzy_match_count}).")

if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    init_master_tables(conn)
    import_master_data(conn)
    generate_links(conn)
    conn.close()
    print("Parts Master Integration complete.")
