import urllib.request, json
res = json.loads(urllib.request.urlopen('http://localhost:8000/api/search?q=4F162-0545').read())
for p in res['results']:
    if p.get('product', {}).get('product_code') == '4F162-0545':
        for d in p.get('drawings', []):
            if 'KF22-221-1-1.jww' in d['file_path']:
                print(d)
