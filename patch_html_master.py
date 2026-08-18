import re

def patch_html(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    new_master_html = """                <div class="search-field" id="searchMasterContainer" style="width: 100%; margin: 8px 0 0 0;">
                    <label style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                        マスタ情報 (寸法・材質など AND検索)
                        <button type="button" class="btn btn-secondary" id="addMasterBtn" onclick="addMasterInput()" style="padding: 2px 8px; font-size: 14px; border-radius: 4px; height: auto;">＋追加 (最大3つ)</button>
                    </label>
                    <div id="masterInputsList" style="display: flex; flex-direction: row; gap: 8px; width: 100%;">
                        <div class="master-input-row" style="display: flex; gap: 4px; flex: 1;">
                            <input type="text" class="searchMasterInput" placeholder="M3" style="width: 100%;">
                        </div>
                    </div>
                </div>"""

    # find <div class="search-field" id="searchPartContainer" ...> ... </div> </div>
    pattern = re.compile(r'(<div class="search-field" id="searchPartContainer"[\s\S]*?</div>\s*</div>\s*</div>)')
    
    if pattern.search(content):
        if "searchMasterContainer" not in content:
            # We want to insert it right before the last closing </div> in the matched string.
            # But wait, it's easier to just match:
            part_pattern = re.compile(r'(<div class="search-field" id="searchPartContainer"[^>]*>[\s\S]*?</div>\s*</div>\s*</div>)')
            match = part_pattern.search(content)
            if match:
                full_match = match.group(1)
                new_str = full_match + "\n" + new_master_html
                content = content.replace(full_match, new_str)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print("Patched index.html")
        else:
            print("Already patched")
    else:
        print("Failed to patch index.html")

patch_html('templates/index.html')
