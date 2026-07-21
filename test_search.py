import main

main.GLOBAL_CACHE = None
main.build_cache()
res = main.search_api(q='IF226-756', seiban='', req_no='', product='', part_no='')
print(f"Results length: {len(res['results'])}")
if len(res['results']) > 0:
    for g in res['results']:
        print("Found group:")
        print("Drawings:", len(g.get('drawings', [])))
        for d in g.get('drawings', []):
            if 'if226-756' in d.get('link_key', '').lower():
                print("MATCH:", d)
else:
    print("No results!")
    # Check unclassified manually
    unclass = main.GLOBAL_CACHE[-1]
    print("Checking unclassified manually. Drawings count:", len(unclass.get('drawings', [])))
    text = ""
    for d in unclass.get('drawings', []):
        text += main.normalize_text((d.get('link_key', '') or "") + " " + (d.get('file_path', '') or ""))
    print("Is if226-756 in unclass text?", 'if226-756' in text)
    
    # Check why it didn't match in API
    search_q = ['if226-756']
    match_general = True
    for token in search_q:
        if token not in text:
            match_general = False
    print("match_general:", match_general)
    print("unclassified length in GLOBAL_CACHE:", len(main.GLOBAL_CACHE[-1].get('drawings', [])))
