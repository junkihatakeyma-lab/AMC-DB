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
                    # Sometimes the explicit filename is a shorter version of the old_id
                    score += 200
            
    if not spec or not text:
        return score
        
    spec_norm = normalize_text(spec)
    text_norm = normalize_text(text)
    
    # Spec token matching
    tokens = re.split(r'[\s/＊*・]+', str(spec))
    tokens = [normalize_text(tok) for tok in tokens if len(tok.strip()) > 1]
    
    for tok in tokens:
        if tok in text_norm:
            score += len(tok)
            
    # Decode 25-digit ID features for bonus scoring
    if len(new_id) == 25:
        # [15:18] is pleat count (山数)
        pleat_count_str = new_id[15:18]
        if pleat_count_str.isdigit():
            pleat_val = str(int(pleat_count_str))
            if pleat_val != '0':
                if f"{pleat_val}山" in text_norm or f"山数{pleat_val}" in text_norm:
                    score += 100
                elif pleat_val in text_norm:
                    score += 20
                    
        # [18:21] is height
        height_str = new_id[18:21]
        if height_str.isdigit():
            height_val = str(int(height_str))
            if height_val != '0':
                if f"l{height_val}" in text_norm or f"l={height_val}" in text_norm or f"*{height_val}" in text_norm:
                    score += 30
                elif height_val in text_norm:
                    score += 10
                    
        # [1:5] is OD
        diam_str = new_id[1:5]
        if diam_str.isdigit():
            diam_val = str(int(diam_str))
            if diam_val != '0':
                if f"φ{diam_val}" in text_norm or f"{diam_val}φ" in text_norm:
                    score += 30
                elif diam_val in text_norm:
                    score += 10

    return score

print("3F136 BOM:", compute_score("R0137ADMSU0951X1101052001", "3F136.6W-0951", "φ137/φ72*120/0 @W型 @EPDM @SUS304 @SECC @バンド2本締 @接着付", "3F136.6-201A プレートA 3F136-102 プレートB 3F136-104-0580 チューブ 3F136-110 リテーナー 3F136-113 L字 4F162-0805 外装箱 5F137改用 マイクロバンド IF000-BR/ リベット 【特記・赤字】", "3F136.6-0580(#4516).xlsx"))
print("IF253 Request:", compute_score("R0253BSESE0503U1130066001", "IF253-0500", "φ253/φ150*500/0", "IF253-0500(#1234)", "IF253-0500(#1234)"))
