from main import build_cache, GLOBAL_CACHE
if GLOBAL_CACHE is None: build_cache()

g = [x for x in GLOBAL_CACHE if 'IF400=0500' in x['_search_product']]
for x in g[:5]:
    print(f"Product: {x['product'].get('product_code')} BOMs: {len(x.get('boms', []))} Inspec: {len(x.get('inspections', []))}")
