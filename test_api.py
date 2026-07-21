import urllib.request, json
res = urllib.request.urlopen('http://127.0.0.1:8000/api/search?q=IF400').read()
data = json.loads(res)
print('results for IF400:', len(data['results']))
boms = sum(len(r.get('boms', [])) for r in data['results'])
reqs = sum(len(r.get('requests', [])) for r in data['results'])
insps = sum(len(r.get('inspections', [])) for r in data['results'])
print(f"Total BOMs: {boms}, Reqs: {reqs}, Insps: {insps}")
