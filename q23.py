import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for g in data:
    product = g.get('product')
    if product and 'R0203ASESE0545U1025045001' in product.get('product_code', ''):
        print(f"Found R0203ASESE0545U1025045001. BOM count: {len(g.get('boms', []))}")
        for b in g.get('boms', []):
            if '100山' in b.get('file', ''):
                print('FOUND 100山 IN 45山 BOX!!!')
