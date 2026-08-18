import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for g in data:
    product = g.get('product', {})
    if product and product.get('product_code') == 'R0203ASESE0545U1025045001':
        print(f"Found R0203ASESE0545U1025045001. BOM count: {len(g.get('boms', []))}")
    for b in g.get('boms', []):
        if '100山' in b.get('file', ''):
            print(f"FOUND 100山 IN BOX: {product.get('product_code', 'NO_PRODUCT_CODE') if product else 'NO_PRODUCT'}")
        if '114山' in b.get('file', ''):
            print(f"FOUND 114山 IN BOX: {product.get('product_code', 'NO_PRODUCT_CODE') if product else 'NO_PRODUCT'}")
