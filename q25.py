import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for g in data:
    product = g.get('product')
    if product and ('R0203ASESE0545U1025045001' in product.get('product_code', '') or '1025045' in product.get('product_code', '')):
        print(f"Code: {product.get('product_code')}, Name: {product.get('name')}")
