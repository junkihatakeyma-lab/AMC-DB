import sqlite3
import json
import re
import os

def extract_pleat_counts(text):
    if not text: return []
    # Match patterns like 100山, 山数100
    matches = re.findall(r'(\d+)山|山数(\d+)', text)
    pleats = []
    for m in matches:
        if m[0]: pleats.append(m[0])
        elif m[1]: pleats.append(m[1])
    return list(set(pleats))

def normalize_text(t):
    if not t: return ""
    return str(t).lower().replace(' ', '').replace('　', '')

def compute_score(new_id, old_id, spec, text, explicit_filename=""):
    score = 0
    
    if explicit_filename:
        # Get just the filename, not the directory path
        ef_basename = os.path.basename(explicit_filename)
        ef_norm = normalize_text(ef_basename)
        old_id_norm = normalize_text(old_id)
        if ef_norm and old_id_norm:
            if ef_norm == old_id_norm:
                score += 1000
            else:
                # Remove suffixes like .xlsx, .pdf, (#123)
                ef_base = re.sub(r'\(.*?\)', '', ef_norm)
                ef_base = re.sub(r'\.(xlsx|pdf|xls)$', '', ef_base).strip()
                old_base = re.sub(r'\(.*?\)', '', old_id_norm).strip()
                if ef_base and old_base and ef_base == old_base:
                    score += 1000
                elif old_base in ef_base:
                    score += 500
                elif ef_base in old_base:
                    score += 200
            
    if not spec or not text:
        return score
        
    spec_norm = normalize_text(spec)
    text_norm = normalize_text(text)
    full_text = text_norm + " " + normalize_text(os.path.basename(explicit_filename)) if explicit_filename else text_norm
    found_pleats = extract_pleat_counts(full_text)
    
    # Spec token matching
    tokens = re.split(r'[\s/＊*・]+', str(spec))
    tokens = [normalize_text(tok) for tok in tokens if len(tok.strip()) > 1]
    
    for tok in tokens:
        if tok in text_norm:
            score += len(tok)
            
    # Decode 25-digit ID features for bonus scoring
    if len(new_id) == 25:
        # [19:22] is pleat count (山数)
        pleat_count_str = new_id[19:22]
        if pleat_count_str.isdigit():
            pleat_val = str(int(pleat_count_str))
            
            # If we explicitly found a pleat count in the text (like 100山), 
            # and this master's pleat count doesn't match it, strictly reject it.
            if found_pleats and pleat_val not in found_pleats:
                return -9999
                
            if pleat_val != '0':
                if f"{pleat_val}山" in full_text or f"山数{pleat_val}" in full_text:
                    score += 100
                elif pleat_val in full_text:
                    score += 20
                    
        # [10:14] is height
        height_str = new_id[10:14]
        if height_str.isdigit():
            height_val = str(int(height_str))
            if height_val != '0':
                if f"l{height_val}" in full_text or f"l={height_val}" in full_text or f"*{height_val}" in full_text:
                    score += 30
                elif height_val in full_text:
                    score += 10
                    
        # [1:5] is OD
        diam_str = new_id[1:5]
        if diam_str.isdigit():
            diam_val = str(int(diam_str))
            if diam_val != '0':
                if f"φ{diam_val}" in full_text or f"{diam_val}φ" in full_text:
                    score += 30
                elif diam_val in full_text:
                    score += 10

    return score

def main():
    with open('mapping.json', 'r', encoding='utf-8') as f:
        mapping = json.load(f)
        
    conn = sqlite3.connect('部品DB.sqlite')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Clear existing mapping to undo the previous mistake
    c.execute("UPDATE requests SET new_part_no = NULL")
    c.execute("UPDATE boms SET new_part_no = NULL")
    conn.commit()

    # 1. Update Drawings
    print("Updating Drawings...")
    c.execute("SELECT id, file_path, link_key FROM simple_files WHERE type='drawing'")
    drawings = c.fetchall()
    
    for d in drawings:
        fid = d['id']
        path = str(d['file_path'])
        
        m = re.search(r'[A-Z0-9]{25}', path)
        if m:
            new_id = m.group(0)
            c.execute("UPDATE simple_files SET link_key=? WHERE id=?", (new_id, fid))
        else:
            lkey = d['link_key']
            matches = [m for m in mapping if m['old_id'] == lkey]
            if matches:
                new_id = matches[0]['new_id']
                c.execute("UPDATE simple_files SET link_key=? WHERE id=?", (new_id, fid))
    
    # 2. Update Requests
    print("Updating Requests...")
    c.execute("SELECT * FROM requests")
    requests = c.fetchall()
    for req in requests:
        req_no = req['request_no']
        hinmei = req['hinmei']
        dest = req['dest']
        note = req['biko']
        
        req_text = f"{hinmei} {dest} {note}"
        
        best_match = None
        best_score = -1
        
        candidates = []
        for m in mapping:
            old_id_norm = normalize_text(m['old_id'])
            hinmei_norm = normalize_text(hinmei)
            if old_id_norm and (old_id_norm in hinmei_norm or hinmei_norm in old_id_norm):
                candidates.append(m)
                
        if len(candidates) == 1:
            # We still need to check if it's a valid match (score >= 100)
            score = compute_score(candidates[0]['new_id'], candidates[0]['old_id'], candidates[0]['spec'], req_text, hinmei)
            if score >= 100:
                c.execute("UPDATE requests SET new_part_no=? WHERE request_no=?", (candidates[0]['new_id'], req_no))
        elif len(candidates) > 1:
            best_score = 0
            best_match = None
            tied_matches = []
            
            for m in candidates:
                score = 0
                if normalize_text(m['customer']) and normalize_text(m['customer']) in normalize_text(dest):
                    score += 50
                    
                score += compute_score(m['new_id'], m['old_id'], m['spec'], req_text, hinmei)
                
                if score > best_score:
                    best_score = score
                    best_match = m
                    tied_matches = [m]
                elif score == best_score:
                    tied_matches.append(m)
                    
            # Only assign if we found a distinguishing clue (score >= 100) and no tie among the best matches
            if best_match and best_score >= 100 and len(tied_matches) == 1:
                c.execute("UPDATE requests SET new_part_no=? WHERE request_no=?", (best_match['new_id'], req_no))
            
    # 3. Update BOMs
    print("Updating BOMs...")
    c.execute("SELECT * FROM boms")
    boms = c.fetchall()
    
    c.execute("SELECT bom_id, part_no, role FROM bom_components")
    comps = c.fetchall()
    comp_map = {}
    for comp in comps:
        comp_map.setdefault(comp['bom_id'], []).append(f"{comp['part_no']} {comp['role']}")
        
    for bom in boms:
        bom_id = bom['id']
        product_code = bom['product_code']
        
        bom_text = " ".join(comp_map.get(bom_id, []))
        
        best_match = None
        best_score = -1
        
        bom_filename = bom['file'] or ''
        
        candidates = []
        for m in mapping:
            old_id_norm = normalize_text(m['old_id'])
            pc_norm = normalize_text(product_code)
            if old_id_norm and (old_id_norm in pc_norm or pc_norm in old_id_norm):
                candidates.append(m)
                
        if len(candidates) == 1:
            score = compute_score(candidates[0]['new_id'], candidates[0]['old_id'], candidates[0]['spec'], bom_text, bom_filename)
            if score >= 100:
                c.execute("UPDATE boms SET new_part_no=? WHERE id=?", (candidates[0]['new_id'], bom_id))
        elif len(candidates) > 1:
            best_score = 0
            best_match = None
            tied_matches = []
            
            for m in candidates:
                score = compute_score(m['new_id'], m['old_id'], m['spec'], bom_text, bom_filename)
                
                if score > best_score:
                    best_score = score
                    best_match = m
                    tied_matches = [m]
                elif score == best_score:
                    tied_matches.append(m)
                    
            if best_match and best_score >= 100 and len(tied_matches) == 1:
                c.execute("UPDATE boms SET new_part_no=? WHERE id=?", (best_match['new_id'], bom_id))
            
    # 4. Post-Validation for All Mapped BOMs
    print("Post-validating all mapped BOMs...")
    import collections
    
    # Reload mapped BOMs
    c.execute("SELECT id, file, new_part_no FROM boms WHERE new_part_no IS NOT NULL")
    mapped_boms = c.fetchall()
    
    boms_by_new_part_no = collections.defaultdict(list)
    for bom in mapped_boms:
        boms_by_new_part_no[bom['new_part_no']].append(bom)
            
    def get_bom_components(bom_id):
        c.execute("SELECT part_no FROM bom_components WHERE bom_id = ? ORDER BY part_no", (bom_id,))
        return tuple(sorted([row['part_no'] for row in c.fetchall() if row['part_no']]))
        
    unmapped_count = 0
    
    for new_part_no, boms_list in boms_by_new_part_no.items():
        canonical_comps = None
        
        # Try to find a standard BOM first (no # in filename)
        std_boms = [b for b in boms_list if '(#' not in (b['file'] or '') and '（#' not in (b['file'] or '')]
        
        if std_boms:
            canonical_comps = get_bom_components(std_boms[0]['id'])
        else:
            # If no standard BOM exists, use the first BOM in the list as the canonical one
            canonical_comps = get_bom_components(boms_list[0]['id'])
            
        for bom in boms_list:
            bom_id = bom['id']
            comps = get_bom_components(bom_id)
            if comps != canonical_comps:
                c.execute("UPDATE boms SET new_part_no = NULL WHERE id = ?", (bom_id,))
                unmapped_count += 1
            
    print(f"Post-validation: unmapped {unmapped_count} BOMs due to strict component mismatch.")

    conn.commit()
    conn.close()
    print("Migration complete!")

if __name__ == '__main__':
    main()
