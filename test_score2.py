import re

def normalize_text(t):
    if not t: return ""
    return str(t).lower().replace(' ', '').replace('　', '')

def compute_score(new_id, old_id, spec, text, explicit_filename=""):
    score = 0
    
    if explicit_filename:
        ef_norm = normalize_text(explicit_filename)
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
    full_text = text_norm + " " + normalize_text(explicit_filename)
    
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

bom_text = "IF402-001 プレートA IF402B-002 プレートB IF402B-004-0545 チューブ IF220-007F P/K 14F200-0545 外装箱 ラベル 【特記・赤字】"
filename = "IF402B-0545(100山#12004).xlsx"
old_id = "IF402B-0545"

# 79山 master
print("79山:", compute_score("R0203ASESE0545U1120079001", old_id, "φ203/φ90*180/0 @ガスケット付E4385", bom_text, filename))
# 100山 master (I don't have the exact 100山 master string but let's assume it has 100 at 19:22)
print("100山:", compute_score("R0203ASESE0545U1001100001", old_id, "φ203/φ90*180/0 @ガスケット付", bom_text, filename))
