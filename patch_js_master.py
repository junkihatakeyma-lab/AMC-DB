import re

def patch_js(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add addMasterInput function after addPartInput
    add_master_func = """
window.addMasterInput = function(val = '') {
    const list = document.getElementById('masterInputsList');
    const currentInputs = list.querySelectorAll('.master-input-row');
    if (currentInputs.length >= 3) {
        alert('マスタ情報の検索窓は最大3つまでです。');
        return;
    }

    const row = document.createElement('div');
    row.className = 'master-input-row';
    row.style = 'display: flex; gap: 4px; flex: 1;';
    
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'searchMasterInput';
    input.placeholder = '追加のマスタ情報';
    input.value = val;
    input.style = 'width: 100%;';
    input.addEventListener('input', () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(performSearch, 300);
    });

    row.appendChild(input);
    list.appendChild(row);
};
"""
    if "window.addMasterInput =" not in content:
        content = re.sub(r'(window\.addPartInput = function\(val = \'\'\) \{[\s\S]*?\n\})', r'\1\n' + add_master_func, content)
        
    # 2. Add search_master extraction in performSearch
    # Search for: const partInputs = Array.from(document.querySelectorAll('.searchPartInput')).map(i => i.value.trim()).filter(v => v !== '');
    # const part = partInputs.join(' ');
    master_extraction = """
    const masterInputs = Array.from(document.querySelectorAll('.searchMasterInput')).map(i => i.value.trim()).filter(v => v !== '');
    const search_master = masterInputs.map(t => normalize(t));
"""
    if "const search_master =" not in content:
        content = content.replace("const part = partInputs.join(' ');", "const part = partInputs.join(' ');" + master_extraction)

    # 3. Add filtering logic in the filter loop:
    # let match_part = true; ...
    master_filter = """
        let match_master = true;
        if (search_master.length > 0) {
            if (!g.boms || g.boms.length === 0) {
                match_master = false;
            } else {
                match_master = g.boms.some(b => {
                    if (!b.components) return false;
                    return search_master.every(token => {
                        return b.components.some(c => {
                            if (!c.master) return false;
                            const masterStr = `${c.master.hinmei || ''} ${c.master.k_sunpo || ''} ${c.master.zaishitsu || ''}`;
                            return normalize(masterStr).includes(token);
                        });
                    });
                });
            }
        }
"""
    if "let match_master = true;" not in content:
        content = content.replace("let match_part = true;", master_filter + "\n        let match_part = true;")

    # 4. Include match_master in the final condition
    # if (match_seiban && match_req && match_company && match_product && match_part) {
    if "match_part && match_master" not in content:
        content = content.replace("&& match_part)", "&& match_part && match_master)")

    # 5. We also need to filter the boms directly so non-matching BOMs are not rendered.
    # We can inject this where `search_part` filtering on BOMs is done.
    # search_part does NOT filter boms array right now in JS! Wait, does it?
    # No, it just filters groups! And the UI renders all BOMs inside that group!
    # Wait, if we want to ONLY show BOMs that match the master info, we should filter `g_out.boms`.
    # Let's find where `g_out.boms = g.boms.map...` or similar happens.
    # Actually, `search_part` DOES filter BOMs! Let's find it.
    # "if (search_part.length > 0) {" in performSearch...
    bom_master_filter = """
                if (search_master.length > 0) {
                    if (g_out.boms) {
                        g_out.boms = g_out.boms.filter(b => {
                            if (!b.components) return false;
                            return search_master.every(token => {
                                return b.components.some(c => {
                                    if (!c.master) return false;
                                    const masterStr = `${c.master.hinmei || ''} ${c.master.k_sunpo || ''} ${c.master.zaishitsu || ''}`;
                                    return normalize(masterStr).includes(token);
                                });
                            });
                        });
                    }
                }
"""
    if "if (search_master.length > 0) {\n                    if (g_out.boms)" not in content:
        # insert it after `g_out.boms = JSON.parse(JSON.stringify(g.boms));`
        # or after `if (search_part.length > 0) { ... }` inside the cloning logic.
        content = re.sub(
            r'(if \(search_part\.length > 0\) \{[\s\S]*?g_out\.boms = g_out\.boms\.filter\(b => \{[\s\S]*?\}\);\s*\}\s*\})',
            r'\1\n' + bom_master_filter,
            content
        )

    # 6. clearAllSearch modification
    # document.getElementById('searchCompany').value = '';
    clear_master = """
    const masterInputs = document.querySelectorAll('.searchMasterInput');
    if (masterInputs.length > 0) {
        masterInputs[0].value = '';
        for (let i = 1; i < masterInputs.length; i++) {
            masterInputs[i].parentNode.remove();
        }
    }
"""
    if "const masterInputs =" not in content:
        content = content.replace("document.getElementById('searchCompany').value = '';", "document.getElementById('searchCompany').value = '';\n" + clear_master)
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filename}")

patch_js('static/app_raw.js')
patch_js('build_clean_app2.py')
