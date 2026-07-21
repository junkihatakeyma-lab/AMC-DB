import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the start of advanced-search
old_html = """            <div class="advanced-search">
                <div class="search-field">
                    <label>総合検索</label>
                    <div class="input-wrapper">
                        <span class="search-icon">🔍</span>
                        <input type="text" id="searchInput" placeholder="全体からキーワード検索" autofocus>
                    </div>
                </div>
                <div class="search-field">
                    <label>製番</label>
                    <input type="text" id="searchSeiban" placeholder="例: 2606-0131">
                </div>
                <div class="search-field">
                    <label>依頼No</label>
                    <input type="text" id="searchReq" placeholder="例: 11540">
                </div>
                <div class="search-field">
                    <label>図番</label>
                    <input type="text" id="searchDrawing" placeholder="例: KF...">
                </div>
                <div class="search-field">
                    <label>商品名・品名</label>
                    <input type="text" id="searchProduct" placeholder="例: 5F137B">
                </div>
                <div class="search-field" id="searchPartContainer">
                    <label style="display: flex; justify-content: space-between; align-items: center;">
                        部品番号 
                        <button type="button" class="btn btn-secondary" onclick="addPartInput()" style="padding: 2px 8px; font-size: 14px; border-radius: 4px; height: auto;">＋追加</button>
                    </label>
                    <div id="partInputsList" style="display: flex; flex-direction: column; gap: 4px;">
                        <div class="part-input-row" style="display: flex; gap: 4px;">
                            <input type="text" class="searchPartInput" placeholder="例: IF000-304" style="flex: 1;">
                        </div>
                    </div>
                </div>
                <div class="search-field" style="display: flex; align-items: flex-end;">
                    <button class="btn btn-primary" onclick="performSearch()" style="height: 42px; padding: 0 24px; font-weight: bold; border-radius: 8px;">検索</button>
                    <button class="btn btn-secondary" onclick="clearAllSearch()" style="height: 42px; padding: 0 16px; margin-left: 8px; border-radius: 8px;">クリア</button>
                </div>
            </div>"""

new_html = """            <div style="display: flex; flex-direction: column; gap: 16px; margin-top: 20px; width: 100%;">
                <div class="advanced-search" style="margin-top: 0;">
                    <div class="search-field">
                        <label>総合検索</label>
                        <div class="input-wrapper">
                            <span class="search-icon">🔍</span>
                            <input type="text" id="searchInput" placeholder="全体からキーワード検索" autofocus>
                        </div>
                    </div>
                    <div class="search-field">
                        <label>製番</label>
                        <input type="text" id="searchSeiban" placeholder="例: 2606-0131">
                    </div>
                    <div class="search-field">
                        <label>依頼No</label>
                        <input type="text" id="searchReq" placeholder="例: 11540">
                    </div>
                    <div class="search-field">
                        <label>図番</label>
                        <input type="text" id="searchDrawing" placeholder="例: KF...">
                    </div>
                    <div class="search-field">
                        <label>商品名・品名</label>
                        <input type="text" id="searchProduct" placeholder="例: 5F137B">
                    </div>
                    <div class="search-field" style="display: flex; align-items: flex-end;">
                        <button class="btn btn-primary" onclick="performSearch()" style="height: 42px; padding: 0 24px; font-weight: bold; border-radius: 8px;">検索</button>
                        <button class="btn btn-secondary" onclick="clearAllSearch()" style="height: 42px; padding: 0 16px; margin-left: 8px; border-radius: 8px;">クリア</button>
                    </div>
                </div>
                
                <div class="search-field" id="searchPartContainer" style="width: 100%; margin: 0;">
                    <label style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                        部品番号 (AND検索)
                        <button type="button" class="btn btn-secondary" id="addPartBtn" onclick="addPartInput()" style="padding: 2px 8px; font-size: 14px; border-radius: 4px; height: auto;">＋追加 (最大5つ)</button>
                    </label>
                    <div id="partInputsList" style="display: flex; flex-direction: row; gap: 8px; width: 100%;">
                        <div class="part-input-row" style="display: flex; gap: 4px; flex: 1;">
                            <input type="text" class="searchPartInput" placeholder="例: IF000-304" style="width: 100%;">
                        </div>
                    </div>
                </div>
            </div>"""

if old_html in content:
    content = content.replace(old_html, new_html)
else:
    print("WARNING: Could not find exact HTML block to replace in index.html")

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.html")
