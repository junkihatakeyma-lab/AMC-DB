with open('deploy_to_firebase.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace the grouping logic
code = code.replace(
'''    # 1. Fetch all Products
    c.execute("SELECT * FROM products")
    products = [dict(row) for row in c.fetchall()]
    
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
        grouped[p['product_code']]['seibans'] = [row['seiban'] for row in c.fetchall()]''',
'''    # 1. Fetch all Products
    c.execute("SELECT * FROM products")
    products = {row['product_code']: dict(row) for row in c.fetchall()}
    
    c.execute("SELECT * FROM seibans")
    seibans_list = [dict(row) for row in c.fetchall()]
    seibans_by_pcode = defaultdict(list)
    for s in seibans_list:
        if s['product_code']:
            seibans_by_pcode[s['product_code']].append(s['seiban'])

    grouped = {}
    unclassified = {
        'new_part_no': '未分類',
        'product': None,
        'seibans': [],
        'boms': [],
        'requests': [],
        'inspections': [],
        'photos': [],
        'drawings': []
    }
    
    def get_or_create_group(key, pcode=None):
        if not key:
            key = '未分類'
        if key == '未分類':
            return unclassified
        if key not in grouped:
            prod = products.get(pcode) if pcode else None
            if not prod and key in products:
                prod = products[key]
            seibans = seibans_by_pcode.get(pcode, []) if pcode else []
            if not seibans and key in seibans_by_pcode:
                seibans = seibans_by_pcode[key]
                
            grouped[key] = {
                'new_part_no': key,
                'product': prod,
                'seibans': seibans,
                'boms': [],
                'requests': [],
                'inspections': [],
                'photos': [],
                'drawings': []
            }
        return grouped[key]
''')

# We need to replace the boms assignment to grouped.
code = code.replace(
'''        if bdict['product_code'] and bdict['product_code'] in grouped:
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
            unclassified['boms'].append(bdict)''',
'''        key = bdict.get('new_part_no') or bdict.get('product_code') or '未分類'
        grp = get_or_create_group(key, bdict.get('product_code'))
        if not grp.get('product') and bdict.get('product_code'):
             grp['product'] = {'product_code': bdict['product_code'], 'name': '未登録製品', 'alias': ''}
        grp['boms'].append(bdict)
        for req_no in bdict['ref_requests']:
            req_to_pcode[req_no] = key''')

# We need to replace the requests assignment
code = code.replace(
'''        assigned_pcode = req_to_pcode.get(rdict['request_no'])
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
            grouped[vid]['requests'].append(rdict)''',
'''        assigned_key = rdict.get('new_part_no') or req_to_pcode.get(rdict['request_no'])
        if not assigned_key:
            base_req_no = re.sub(r'\D', '', str(rdict['request_no']))
            assigned_key = req_to_pcode.get(base_req_no)
            
        key = assigned_key or rdict.get('hinmei') or rdict.get('request_no') or '未分類'
        grp = get_or_create_group(key)
        if not grp.get('product'):
            grp['product'] = {'product_code': key, 'name': '未登録製品(依頼書)', 'alias': ''}
        grp['requests'].append(rdict)''')

# Simple files
code = code.replace(
'''        pcode = sdict['link_key']
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
                
        target = grouped[actual_pcode] if actual_pcode else unclassified''',
'''        key = sdict.get('link_key') or '未分類'
        target = get_or_create_group(key)
        if not target.get('product') and key != '未分類':
            target['product'] = {'product_code': key, 'name': '未登録部品', 'alias': ''}''')

with open('deploy_to_firebase.py', 'w', encoding='utf-8') as f:
    f.write(code)
