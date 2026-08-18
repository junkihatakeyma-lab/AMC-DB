import re
import json
import codecs

def fix_mojibake():
    with open('static/app.js.bak', 'r', encoding='utf-8') as f:
        old_js = f.read()
        
    with open('static/app.js', 'r', encoding='utf-8', errors='replace') as f:
        new_js = f.read()

    # Create mapping of UI code to Japanese strings from the old file
    # We will just manually replace known corrupted fragments.
    replacements = [
        # Search normalization
        (r't = t.replace\(\/\[.*?\]\/g\, function\(s\) \{', r't = t.replace(/[Ａ-Ｚａ-ｚ０-９]/g, function(s) {'),
        (r't = t.replace\(\/\[.*?\]\/g\, \'#\'\).replace\(\/\[.*?\]\/g\, \'-\'\);', r"t = t.replace(/[＃]/g, '#').replace(/[ー−―‐]/g, '-');"),
        
        # UI Strings
        (r'innerHTML = \'<div class="empty-state">.*?</div>\';', r"innerHTML = '<div class=\"empty-state\">検索条件を入力してください</div>';"),
        (r'statsContainer.textContent = `.*? \$\{totalHits\} .*?`;', r"statsContainer.textContent = `全体で ${totalHits} 件ヒットしました`;"),
        (r'html \+= `<div class="flat-section"><h3>.*? BOM.*? \(\$\{allBoms.length\}.*?</h3>`;', r'html += `<div class="flat-section"><h3>📑 BOM一覧 (${allBoms.length}件)</h3>`;'),
        (r'compsHtml = `<div class="table-wrap" style="margin-bottom:1rem"><table><tr><th>.*?</th><th>.*?</th><th>.*?</th></tr>`;', r'compsHtml = `<div class="table-wrap" style="margin-bottom:1rem"><table><tr><th>役割</th><th>部品番号</th><th>仕様メモ</th></tr>`;'),
        (r"let isRedText = c.role === '.*?';", r"let isRedText = c.role === '【特記・赤字】';"),
        (r'製番: \$\{highlight\(b.seiban, tokens\)\} \| 品名: \$\{highlight\(b._product && b._product.name, tokens\)\}', r'製番: ${highlight(b.seiban, tokens)} | 品名: ${highlight(b._product && b._product.name, tokens)}'),
        
        # Buttons
        (r"onclick='openPreview\(\$\{escapeHtml\(JSON.stringify\(b.previews\)\)\}, \$\{escapeHtml\(JSON.stringify\(b.file\)\)\}\)'>.*?</button>", r"onclick='openPreview(${escapeHtml(JSON.stringify(b.previews))}, ${escapeHtml(JSON.stringify(b.file))})'>プレビュー</button>"),
        (r"onclick='openPreview\(\$\{escapeHtml\(JSON.stringify\(r.previews\)\)\}, \$\{escapeHtml\(JSON.stringify\(r.file\)\)\}\)'>.*?</button>", r"onclick='openPreview(${escapeHtml(JSON.stringify(r.previews))}, ${escapeHtml(JSON.stringify(r.file))})'>プレビュー</button>"),
        (r"onclick='openPreview\(\$\{escapeHtml\(JSON.stringify\(i.previews\)\)\}, \$\{escapeHtml\(JSON.stringify\(i.file_path\)\)\}\)'>.*?</button>", r"onclick='openPreview(${escapeHtml(JSON.stringify(i.previews))}, ${escapeHtml(JSON.stringify(i.file_path))})'>プレビュー</button>"),
        (r"onclick='openPreview\(\$\{escapeHtml\(JSON.stringify\(d.previews\)\)\}, \$\{escapeHtml\(JSON.stringify\(d.file_path\)\)\}\)'>.*?</button>` : ''}", r"onclick='openPreview(${escapeHtml(JSON.stringify(d.previews))}, ${escapeHtml(JSON.stringify(d.file_path))})'>プレビュー</button>` : ''}"),
        
        (r'\(Excel for Web\)</a>` : \(b.file \? `<a href=".*?target="_blank" class="btn btn-secondary">.*?</a>` : \'\'\)', r'(Excel for Web)</a>` : (b.file ? `<a href="/${b.file.replace(/\\\\/g, \'/\').split(\'/\').map(encodeURIComponent).join(\'/\')}" target="_blank" class="btn btn-secondary">Excelを開く</a>` : \'\')'),
        (r'\(Excel for Web\)</a>` : \(r.file \? `<a href=".*?target="_blank" class="btn btn-secondary">.*?</a>` : \'\'\)', r'(Excel for Web)</a>` : (r.file ? `<a href="/${r.file.replace(/\\\\/g, \'/\').split(\'/\').map(encodeURIComponent).join(\'/\')}" target="_blank" class="btn btn-secondary">Excel/画像を開く</a>` : \'\')'),
        (r'\(Excel for Web\)</a>` : \(i.file_path \? `<a href=".*?target="_blank" class="btn btn-secondary">.*?</a>` : \'\'\)', r'(Excel for Web)</a>` : (i.file_path ? `<a href="/${i.file_path.replace(/\\\\/g, \'/\').split(\'/\').map(encodeURIComponent).join(\'/\')}" target="_blank" class="btn btn-secondary">開く</a>` : \'\')'),
        (r'`<a href="\/\$\{p.file_path.replace.*?target="_blank" class="btn btn-secondary">.*?</a>` : \'\'', r'`<a href="/${p.file_path.replace(/\\\\/g, \'/\').split(\'/\').map(encodeURIComponent).join(\'/\')}" target="_blank" class="btn btn-secondary">開く</a>` : \'\''),
        (r'`<a href="\/\$\{d.file_path.replace.*?target="_blank" class="btn btn-secondary">.*?</a>` : \'\'', r'`<a href="/${d.file_path.replace(/\\\\/g, \'/\').split(\'/\').map(encodeURIComponent).join(\'/\')}" target="_blank" class="btn btn-secondary">ダウンロード / 開く</a>` : \'\''),
        
        (r"const pCode = p._product \? p._product.product_code : '.*?';", r"const pCode = p._product ? p._product.product_code : '未分類';"),
        (r"const pCode = d._product \? d._product.product_code : '.*?';", r"const pCode = d._product ? d._product.product_code : '未分類';"),
        
        (r'<p style="font-size:0.85rem; color:var\(--text-muted\); margin: 0 0 0.5rem 0;">.*?: \$\{escapeHtml\(pCode\)\}\$\{escapeHtml\(pName\)\}</p>', r'<p style="font-size:0.85rem; color:var(--text-muted); margin: 0 0 0.5rem 0;">関連製品: ${escapeHtml(pCode)} ${escapeHtml(pName)}</p>'),
        
        (r'html \+= `<div class="flat-section"><h3>.*? \(\$\{allReqs.length\}.*?</h3>`;', r'html += `<div class="flat-section"><h3>📝 加工依頼書一覧 (${allReqs.length}件)</h3>`;'),
        (r'html \+= `<div class="flat-section"><h3>.*? \(\$\{allInsps.length\}.*?</h3><div style="display:flex; flex-wrap:wrap; gap:1rem">`;', r'html += `<div class="flat-section"><h3>📄 検査証一覧 (${allInsps.length}件)</h3><div style="display:flex; flex-wrap:wrap; gap:1rem">`;'),
        (r'html \+= `<div class="flat-section"><h3>.*? \(\$\{allPhotos.length\}.*?</h3><div style="display:flex; flex-wrap:wrap; gap:1rem">`;', r'html += `<div class="flat-section"><h3>📷 写真・その他一覧 (${allPhotos.length}件)</h3><div style="display:flex; flex-wrap:wrap; gap:1rem">`;'),
        (r'html \+= `<div class="flat-section"><h3>.*? \(\$\{allDrawings.length\}.*?</h3><div style="display:flex; flex-wrap:wrap; gap:1rem">`;', r'html += `<div class="flat-section"><h3>📐 図面一覧 (${allDrawings.length}件)</h3><div style="display:flex; flex-wrap:wrap; gap:1rem">`;'),
        
        (r"const isModified = r.file && \(r.file.includes\('.*?'\) \|\| r.file.includes\('.*?'\) \|\| r.file.includes\('.*?'\)\);", r"const isModified = r.file && (r.file.includes('～') || r.file.includes('・') || r.file.includes('修正'));"),
        (r"\$\{r.is_handwritten \? '<span class=\"badge badge-warn\" style=\"margin-left: 8px;\">.*?</span>' : ''\}", r"${r.is_handwritten ? '<span class=\"badge badge-warn\" style=\"margin-left: 8px;\">✍️手書き・要確認</span>' : ''}"),
        (r"\$\{isModified \? '<span class=\"badge badge-warn\" style=\"margin-left: 8px; background: #e74c3c;\">.*?</span>' : ''\}", r"${isModified ? '<span class=\"badge badge-warn\" style=\"margin-left: 8px; background: #e74c3c;\">⚠️修正/関連あり</span>' : ''}"),
        
        (r'<tr><th>.*?</th><td>\$\{highlight\(r.hinmei, tokens\)\}</td><th>.*?</th><td>\$\{highlight\(r.qty, tokens\)\}</td></tr>', r'<tr><th>品名</th><td>${highlight(r.hinmei, tokens)}</td><th>数量</th><td>${highlight(r.qty, tokens)}</td></tr>'),
        (r'<tr><th>.*?</th><td>\$\{highlight\(r.kiji, tokens\)\}</td><th>.*?</th><td>\$\{highlight\(r.yoto, tokens\)\}</td></tr>', r'<tr><th>生地</th><td>${highlight(r.kiji, tokens)}</td><th>用途</th><td>${highlight(r.yoto, tokens)}</td></tr>'),
        (r'<tr><th>.*?</th><td colspan="3">\$\{highlight\(r.spec, tokens\)\}</td></tr>', r'<tr><th>仕様</th><td colspan="3">${highlight(r.spec, tokens)}</td></tr>'),
        (r'<tr><th>.*?</th><td colspan="3">\$\{highlight\(r.biko, tokens\)\}</td></tr>', r'<tr><th>備考</th><td colspan="3">${highlight(r.biko, tokens)}</td></tr>'),
        
        (r"\$\{r.is_handwritten \? `<button class=\"btn btn-secondary\" onclick=\"updateHinmei\('\$\{escapeHtml\(r.request_no\)\}', '\$\{escapeHtml\(r.hinmei\)\}'\)\">.*?</button>` : ''\}", r"${r.is_handwritten ? `<button class=\"btn btn-secondary\" onclick=\"updateHinmei('${escapeHtml(r.request_no)}', '${escapeHtml(r.hinmei)}')\">品名を編集</button>` : ''}"),
        
        (r"html = '<div class=\"empty-state\">.*?</div>';", r"html = '<div class=\"empty-state\">チェックされた項目に該当するデータがありません</div>';"),
        (r"modalBody.innerHTML = '<div style=\"text-align:center;padding:2rem\">.*?</div>';", r"modalBody.innerHTML = '<div style=\"text-align:center;padding:2rem\">プレビュー画像がありません（PDF変換待ち、または未生成です）</div>';"),
        
        (r"alert\('.*?'\);", r"alert('処理が完了しました/エラーが発生しました。リロードします。');"),
        
        # New link UI logic that wasn't in backup
        (r"<button class=\"btn btn-secondary\" style=\"padding: 1px 4px; font-size: 11px; margin-left: 4px;\" onclick=\"openLinkModal\('\$\{escapeHtml\(c.part_no\).replace\(/'/g, \"\\\\\\\\\"\"\)'\)\">.*?</button>", r"<button class=\"btn btn-secondary\" style=\"padding: 1px 4px; font-size: 11px; margin-left: 4px;\" onclick=\"openLinkModal('${escapeHtml(c.part_no).replace(/'/g, \"\\\\'\")}')\">📝紐付</button>"),
        (r"document.getElementById\('linkModalError'\).innerText = '.*?';", r"document.getElementById('linkModalError').innerText = 'マスタ部品番号を入力してください';"),
    ]
    
    for pat, rep in replacements:
        new_js = re.sub(pat, rep, new_js)
        
    with open('static/app.js', 'w', encoding='utf-8') as f:
        f.write(new_js)
        
if __name__ == '__main__':
    fix_mojibake()
