from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Optional
import sqlite3
import re
import os
from database import get_db
from collections import defaultdict

app = FastAPI(title="部品検索DB")

# Serve static files and data files for preview
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/data", StaticFiles(directory="data"), name="data")
app.mount("/previews", StaticFiles(directory="previews"), name="previews")

def safe_str(val):
    if val is None:
        return ""
    return str(val)

def normalize_text(text) -> str:
    text = safe_str(text)
    if not text:
        return ""
    # Convert to lowercase
    text = text.lower()
    # Normalize full-width to half-width for alphanumeric
    text = text.translate(str.maketrans(
        'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ０１２３４５６７８９',
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    ))
    # Normalize # variations
    text = re.sub(r'[＃♯]', '#', text)
    # Normalize hyphens
    text = re.sub(r'[‐－―ー−]', '-', text)
    return text

@app.get("/")
def read_index():
    return FileResponse("templates/index.html")

# Global Cache
GLOBAL_CACHE = None

def build_cache():
    global GLOBAL_CACHE
    conn = get_db()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Bulk fetch components
    c.execute("SELECT * FROM bom_components")
    all_components = c.fetchall()
    bom_comps_map = defaultdict(list)
    for comp in all_components:
        bom_comps_map[comp['bom_id']].append(dict(comp))
        
    # Bulk fetch bom requests
    c.execute("SELECT * FROM bom_requests")
    all_bom_reqs = c.fetchall()
    bom_reqs_map = defaultdict(list)
    for br in all_bom_reqs:
        bom_reqs_map[br['bom_id']].append(br['request_no'])
        
    # Bulk fetch previews
    c.execute("SELECT * FROM previews ORDER BY page_num")
    all_previews = c.fetchall()
    preview_map = defaultdict(list)
    for p in all_previews:
        preview_map[p['file_path']].append(p['preview_path'])
        
    # 1. Fetch all Products
    c.execute("SELECT * FROM products")
    products = [dict(row) for row in c.fetchall()]
    
    # Grouping structure
    grouped = {}

    for p in products:
        grouped[p['product_code']] = {
            'product': p,
            'seibans': [],
            'boms': [],
            'requests': [],
            'inspections': [],
            'photos': [],
            'drawings': []
        }
    
    unclassified = {
        'product': None,
        'seibans': [],
        'boms': [],
        'requests': [],
        'inspections': [],
        'photos': [],
        'drawings': []
    }

    for p in products:
        c.execute("SELECT seiban FROM seibans WHERE product_code=?", (p['product_code'],))
        grouped[p['product_code']]['seibans'] = [row['seiban'] for row in c.fetchall()]

    # Bulk fetch exceptions
    c.execute("SELECT * FROM exceptions")
    all_exceptions = c.fetchall()
    exc_map = {row['file_path']: row['raw_text'] for row in all_exceptions}

    # 2. Fetch all Boms and components
    c.execute("SELECT * FROM boms")
    boms_rows = c.fetchall()
    
    boms = []
    req_to_pcode = {}
    for brow in boms_rows:
        bdict = dict(brow)
        comps = bom_comps_map.get(bdict['id'], [])
        bdict['is_exception'] = bdict['file'] in exc_map
        if not comps and bdict['is_exception']:
            bdict['components'] = exc_map.get(bdict['file'])
        elif not comps and not bdict['layout_ok']:
            bdict['components'] = "【AI解析エラー】データが取得できませんでした"
        else:
            bdict['components'] = comps
            
        bdict['ref_requests'] = bom_reqs_map.get(bdict['id'], [])
        
        db_previews = preview_map.get(bdict['file'], [])
        bdict['previews'] = db_previews if db_previews else ['previews/dummy_0.png']
        import urllib.parse
        SHAREPOINT_BOM_BASE_URL = "https://amcfilter.sharepoint.com/sites/msteams_5b202a/Shared Documents/生産DB/BOM/"
        sp_url = ""
        if bdict['file'].startswith('data/BOM'):
            filename = os.path.basename(bdict['file'])
            # encode filename for URL
            quoted = urllib.parse.quote(filename)
            sp_url = f"{SHAREPOINT_BOM_BASE_URL}{quoted}?web=1" if filename.lower().endswith(('.xls', '.xlsx')) else f"{SHAREPOINT_BOM_BASE_URL}{quoted}"
        bdict['sp_url'] = sp_url

        boms.append(bdict)
        
        if bdict['product_code'] and bdict['product_code'] in grouped:
            grouped[bdict['product_code']]['boms'].append(bdict)
            for req_no in bdict['ref_requests']:
                req_to_pcode[req_no] = bdict['product_code']
        elif bdict['product_code']:
            vid = f"v_{bdict['product_code']}"
            if vid not in grouped:
                grouped[vid] = {'product': {'product_code': bdict['product_code'], 'name': '未登録製品', 'alias': ''}, 'seibans': [], 'boms': [], 'requests': [], 'inspections': [], 'photos': [], 'drawings': []}
            grouped[vid]['boms'].append(bdict)
            for req_no in bdict['ref_requests']:
                req_to_pcode[req_no] = vid
        else:
            unclassified['boms'].append(bdict)
            
    # 3. Fetch all Requests
    c.execute("SELECT * FROM requests")
    requests_rows = c.fetchall()
    requests = []
    for rrow in requests_rows:
        rdict = dict(rrow)
        if 'is_handwritten' not in rdict:
            rdict['is_handwritten'] = 0
        db_previews = preview_map.get(rdict['file'], [])
        fp = rdict.get('file')
        rdict['previews'] = db_previews if db_previews else ([fp] if fp and (fp.lower().endswith('.jpg') or fp.lower().endswith('.png')) else ['previews/dummy_0.png'])
        
        sp_url = ""
        if rdict['file'].startswith('data/加工依頼書_自動読取'):
            filename = os.path.basename(rdict['file'])
            SHAREPOINT_REQ_BASE_URL = "https://amcfilter.sharepoint.com/sites/msteams_5b202a/Shared Documents/生産DB/加工依頼書_手書き/"
            quoted = urllib.parse.quote(filename)
            sp_url = f"{SHAREPOINT_REQ_BASE_URL}{quoted}?web=1" if filename.lower().endswith(('.xls', '.xlsx')) else f"{SHAREPOINT_REQ_BASE_URL}{quoted}"
        elif rdict['file'].startswith('data/加工依頼書'):
            filename = os.path.basename(rdict['file'])
            SHAREPOINT_REQ_BASE_URL = "https://amcfilter.sharepoint.com/sites/msteams_5b202a/Shared Documents/生産DB/加工依頼書/"
            quoted = urllib.parse.quote(filename)
            sp_url = f"{SHAREPOINT_REQ_BASE_URL}{quoted}?web=1" if filename.lower().endswith(('.xls', '.xlsx')) else f"{SHAREPOINT_REQ_BASE_URL}{quoted}"
        rdict['sp_url'] = sp_url

        requests.append(rdict)
        
        assigned_pcode = req_to_pcode.get(rdict['request_no'])
        if not assigned_pcode:
            base_req_no = re.sub(r'\D', '', str(rdict['request_no']))
            assigned_pcode = req_to_pcode.get(base_req_no)
        if not assigned_pcode:
            for pcode in grouped:
                if rdict['hinmei'] and pcode in rdict['hinmei']:
                    assigned_pcode = pcode
                    break
        if assigned_pcode and assigned_pcode in grouped:
            grouped[assigned_pcode]['requests'].append(rdict)
        else:
            key = rdict['hinmei'] or rdict['request_no'] or "unknown"
            vid = f"v_req_{key}"
            if vid not in grouped:
                grouped[vid] = {'product': {'product_code': key, 'name': '未登録製品(依頼書)', 'alias': ''}, 'seibans': [], 'boms': [], 'requests': [], 'inspections': [], 'photos': [], 'drawings': []}
            grouped[vid]['requests'].append(rdict)

    # 4. Fetch Simple Files
    c.execute("SELECT * FROM simple_files")
    sfiles_rows = c.fetchall()
    for srow in sfiles_rows:
        sdict = dict(srow)
        db_previews = preview_map.get(sdict['file_path'], [])
        sdict['previews'] = db_previews if db_previews else ['previews/dummy_0.png']
        
        sp_url = ""
        if sdict['type'] == 'inspection' and sdict['file_path']:
            filename = os.path.basename(sdict['file_path'])
            SHAREPOINT_INSP_BASE_URL = "https://amcfilter.sharepoint.com/sites/msteams_5b202a/Shared Documents/生産DB/検査証/"
            quoted = urllib.parse.quote(filename)
            sp_url = f"{SHAREPOINT_INSP_BASE_URL}{quoted}?web=1" if filename.lower().endswith(('.xls', '.xlsx')) else f"{SHAREPOINT_INSP_BASE_URL}{quoted}"
        elif sdict['type'] == 'drawing' and sdict['file_path']:
            filename = os.path.basename(sdict['file_path'])
            SHAREPOINT_DRAW_BASE_URL = "https://amcfilter.sharepoint.com/sites/msteams_5b202a/Shared Documents/生産DB/図面/"
            quoted = urllib.parse.quote(filename)
            sp_url = f"{SHAREPOINT_DRAW_BASE_URL}{quoted}?web=1" if filename.lower().endswith(('.xls', '.xlsx')) else f"{SHAREPOINT_DRAW_BASE_URL}{quoted}"
        sdict['sp_url'] = sp_url
        
        pcode = sdict['link_key']
        actual_pcode = None
        if pcode in grouped:
            actual_pcode = pcode
        else:
            c.execute("SELECT product_code FROM seibans WHERE seiban=? OR request_no=?", (pcode, pcode))
            res = c.fetchone()
            if res and res['product_code'] in grouped:
                actual_pcode = res['product_code']
                
        if not actual_pcode and pcode:
            vid = f"v_{pcode}"
            if vid not in grouped:
                grouped[vid] = {'product': {'product_code': pcode, 'name': '未登録部品', 'alias': ''}, 'seibans': [], 'boms': [], 'requests': [], 'inspections': [], 'photos': [], 'drawings': []}
            actual_pcode = vid
                
        target = grouped[actual_pcode] if actual_pcode else unclassified
        if sdict['type'] == 'inspection':
            target['inspections'].append(sdict)
        elif sdict['type'] == 'drawing':
            target['drawings'].append(sdict)
        else:
            target['photos'].append(sdict)

    conn.close()
    
    GLOBAL_CACHE = list(grouped.values()) + [unclassified]
    
    # Pre-compute search strings for all items to make search ultra-fast
    for g in GLOBAL_CACHE:
        # Seiban
        seiban_text = " ".join(safe_str(x) for x in g.get('seibans', []))
        for b in g.get('boms', []):
            seiban_text += " " + safe_str(b.get('seiban'))
        g['_search_seiban'] = normalize_text(seiban_text)
        
        # Req
        req_text = ""
        for b in g.get('boms', []):
            req_text += " ".join(safe_str(x) for x in b.get('ref_requests', [])) + " "
        for r in g.get('requests', []):
            req_text += safe_str(r.get('request_no')) + " "
        g['_search_req'] = normalize_text(req_text)
        
        # Product
        p_dict = g.get('product') or {}
        p_text = safe_str(p_dict.get('product_code')) + " " + safe_str(p_dict.get('name')) + " " + safe_str(p_dict.get('alias'))
        g['_search_product'] = normalize_text(p_text)
        
        # Part
        part_text = ""
        for b in g.get('boms', []):
            comps = b.get('components', [])
            if isinstance(comps, str):
                part_text += safe_str(comps) + " "
            else:
                for c_comp in comps:
                    part_text += safe_str(c_comp.get('part_no')) + " "
        for d in g.get('drawings', []):
            part_text += safe_str(d.get('link_key')) + " "
        g['_search_part'] = normalize_text(part_text)
        
        # Company
        company_text = ""
        for r in g.get('requests', []):
            company_text += safe_str(r.get('dest')) + " "
        g['_search_company'] = normalize_text(company_text)
        
        # General
        general_text = p_text + " " + seiban_text + " " + req_text + " " + part_text
        for b in g.get('boms', []):
            comps = b.get('components', [])
            if isinstance(comps, str):
                general_text += " " + safe_str(comps)
            else:
                for c_comp in comps:
                    general_text += " " + safe_str(c_comp.get('role'))
        for r in g.get('requests', []):
            general_text += " " + safe_str(r.get('hinmei'))
        for d in g.get('drawings', []):
            general_text += " " + safe_str(d.get('file_path'))
        g['_search_text'] = normalize_text(general_text)

    return GLOBAL_CACHE


@app.post("/api/clear_cache")
def clear_cache_api():
    global GLOBAL_CACHE
    GLOBAL_CACHE = None
    return {"status": "ok"}

@app.get("/api/search")
def search_api(q: str = Query(""), seiban: str = Query(""), req_no: str = Query(""), product: str = Query(""), part_no: str = Query(""), company: str = Query("")):
    global GLOBAL_CACHE
    if GLOBAL_CACHE is None:
        build_cache()
        
    search_q = normalize_text(q).split() if q else []
    search_seiban = normalize_text(seiban) if seiban else ""
    search_req = normalize_text(req_no) if req_no else ""
    search_product = normalize_text(product) if product else ""
    search_part = normalize_text(part_no).split() if part_no else []
    search_company = normalize_text(company) if company else ""

    results = []
    
    for g in GLOBAL_CACHE:
        if not (g.get('boms') or g.get('requests') or g.get('inspections') or g.get('photos') or g.get('drawings')):
            continue
            
        match_seiban = True
        match_req = True
        match_product = True
        match_part = True
        match_company = True
        match_general = True
        
        if search_seiban and search_seiban not in g['_search_seiban']:
            match_seiban = False
            
        if search_req and search_req not in g['_search_req']:
            match_req = False
            
        if search_product and search_product not in g['_search_product']:
            match_product = False
            
        if search_part:
            for token in search_part:
                if token not in g['_search_part']:
                    match_part = False
                    break
            
        if search_company and search_company not in g.get('_search_company', ''):
            match_company = False
            
        if search_q:
            for token in search_q:
                if token not in g['_search_text']:
                    match_general = False
                    break
                    
        if match_seiban and match_req and match_product and match_part and match_company and match_general:
            g_out = dict(g)
            
            # Filter inner lists based on specific field searches to reduce noise
            if search_req and g.get('requests'):
                g_out['requests'] = [r for r in g['requests'] if search_req in normalize_text(str(r.get('request_no', '')))]
                
            # Limit requests in unclassified group to prevent massive payload
            if g_out.get('product') is None and g_out.get('requests'):
                def _get_req_num(r):
                    import re
                    m = re.search(r'\d+', str(r.get('request_no', '')))
                    return int(m.group()) if m else 0
                g_out['requests'] = sorted(g_out['requests'], key=_get_req_num, reverse=True)[:100]
                
            if search_seiban and g.get('boms'):
                g_out['boms'] = [b for b in g['boms'] if search_seiban in normalize_text(str(b.get('seiban', '')))]
                
            if search_part and g_out.get('boms'): # Use g_out in case it was already filtered by seiban
                filtered_boms = []
                for b in g_out['boms']:
                    comps = b.get('components', [])
                    has_all_tokens = True
                    for token in search_part:
                        if not any(token in normalize_text(str(c.get('part_no', ''))) for c in comps):
                            has_all_tokens = False
                            break
                    if has_all_tokens:
                        filtered_boms.append(b)
                g_out['boms'] = filtered_boms
                


            results.append(g_out)
            if len(results) >= 200:
                break
                
    conn = get_db()
    c = conn.cursor()
    all_files = set()
    for g in results:
        for b in g.get('boms', []): all_files.add(b.get('file'))
        for r in g.get('requests', []): all_files.add(r.get('file'))
        for i in g.get('inspections', []): all_files.add(i.get('file_path'))
        for d in g.get('drawings', []): all_files.add(d.get('file_path'))
    all_files = {f for f in all_files if f}
    
    if all_files:
        placeholders = ','.join('?' for _ in all_files)
        c.execute(f"SELECT file_path, preview_path FROM previews WHERE file_path IN ({placeholders}) ORDER BY page_num", list(all_files))
        dyn_previews = defaultdict(list)
        for row in c.fetchall():
            dyn_previews[row['file_path']].append(row['preview_path'])
            
        for g in results:
            g['boms'] = [dict(b) for b in g.get('boms', [])]
            for b in g['boms']:
                fp = b.get('file')
                b['previews'] = dyn_previews.get(fp) if dyn_previews.get(fp) else ['previews/dummy_0.png']
                
            g['requests'] = [dict(r) for r in g.get('requests', [])]
            for r in g['requests']:
                fp = r.get('file')
                r['previews'] = dyn_previews.get(fp) if dyn_previews.get(fp) else ([fp] if fp and (fp.lower().endswith('.jpg') or fp.lower().endswith('.png')) else ['previews/dummy_0.png'])
                
            g['inspections'] = [dict(i) for i in g.get('inspections', [])]
            for i in g['inspections']:
                fp = i.get('file_path')
                i['previews'] = dyn_previews.get(fp) if dyn_previews.get(fp) else ['previews/dummy_0.png']
                
            g['drawings'] = [dict(d) for d in g.get('drawings', [])]
            for d in g['drawings']:
                fp = d.get('file_path')
                d['previews'] = dyn_previews.get(fp) if dyn_previews.get(fp) else ['previews/dummy_0.png']
    conn.close()

    has_more = len(results) >= 200
    return {"results": results, "has_more": has_more}

@app.get("/api/reload_cache")
def reload_cache():
    global GLOBAL_CACHE
    GLOBAL_CACHE = None
    build_cache()
    return {"status": "ok"}

@app.post("/api/ai_confirm")
async def ai_confirm(data: dict):
    conn = None
    try:
        conn = get_db()
        c = conn.cursor()
        file_path = data.get("file")
        components = data.get("components")
        
        # BOMのcomponentsを更新する処理が必要であればここに実装
        # とりあえずlayout_okをTrueにする
        c.execute("UPDATE boms SET layout_ok=1 WHERE file=?", (file_path,))
        conn.commit()
        
        global GLOBAL_CACHE
        GLOBAL_CACHE = None
        
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        if conn:
            conn.close()

@app.post("/api/register_product")
async def register_product(data: dict):
    conn = None
    try:
        conn = get_db()
        c = conn.cursor()
        pcode = data.get('product_code')
        name = data.get('name')
        if not pcode or not name:
            return {"status": "error", "message": "Missing fields"}
        
        c.execute("INSERT OR REPLACE INTO products (product_code, name, alias) VALUES (?, ?, ?)", (pcode, name, ''))
        conn.commit()
        
        global GLOBAL_CACHE
        GLOBAL_CACHE = None
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        if conn:
            conn.close()

@app.post("/api/update_hinmei")
async def update_hinmei(data: dict):
    conn = None
    try:
        conn = get_db()
        c = conn.cursor()
        request_no = data.get('request_no')
        new_hinmei = data.get('hinmei')
        if not request_no or new_hinmei is None:
            return {"status": "error", "message": "Missing fields"}
            
        c.execute("UPDATE requests SET hinmei=? WHERE request_no=?", (new_hinmei, request_no))
        conn.commit()
        
        global GLOBAL_CACHE
        GLOBAL_CACHE = None
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# trigger reload

# Trigger API reload

# trigger reload

# trigger reload 2

# trigger reload 3

# trigger reload 4

# trigger reload 5
