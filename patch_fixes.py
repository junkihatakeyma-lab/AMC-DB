import re

def patch_js(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update search_master array creation (allow space separation)
    content = content.replace(
        "const search_master = masterInputs.map(t => normalize(t));",
        "const search_master = masterInputs.join(' ').split(/\\s+/).map(t => normalize(t)).filter(v=>v);"
    )

    # 2. Add master to state object
    content = content.replace(
        "const state = { q, seiban, req_no: req, product, part_no: part, company: company };",
        "const state = { q, seiban, req_no: req, product, part_no: part, company: company, master: masterInputs.join(' ') };"
    )

    # 3. Add highlight to the master info table rendering
    old_master_html = "`品名: ${c.master.hinmei||''}`, `寸法: ${c.master.k_sunpo||''}`, `材質: ${c.master.zaishitsu||''}`].filter(s=>!s.endsWith(': ')).map(s=>escapeHtml(s))"
    new_master_html = "`品名: ${c.master.hinmei||''}`, `寸法: ${c.master.k_sunpo||''}`, `材質: ${c.master.zaishitsu||''}`].filter(s=>!s.endsWith(': ')).map(s=>highlight(s, tokens))"
    content = content.replace(old_master_html, new_master_html)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filename}")

patch_js('static/app_raw.js')
patch_js('build_clean_app2.py')
