import json, glob, sqlite3
reqs = []
for f in glob.glob('chunk_*.json'):
    with open(f, 'r') as fp:
        reqs.extend(json.load(fp))

conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
c = conn.cursor()
skipped = []
for req in reqs:
    res = c.execute("SELECT hinmei FROM requests WHERE request_no=?", (req,)).fetchone()
    if res and res[0] == '':
        skipped.append(req)

print('SKIPPED:', skipped)
