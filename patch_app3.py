import re

with open('static/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update renderProductSearch
old_product_req = """        // Render Requests
        if (group.requests && group.requests.length > 0) {
            // Sort requests descending
            group.requests.sort((a, b) => {
                const numA = parseInt(a.request_no) || 0;
                const numB = parseInt(b.request_no) || 0;
                return numB - numA;
            });
            
            boxHtml += `
                <div class="section">
                    <div class="section-header" onclick="this.parentElement.classList.toggle('open')">
                        <span>📝 加工依頼書 (${group.requests.length}件)</span>
                    </div>
                    <div class="section-content">
                        <div class="section-inner">
            `;
            group.requests.forEach(r => {
                const isModified = r.file && (r.file.includes('〇') || r.file.includes('×') || r.file.includes('修正'));
                boxHtml += `
                    <div class="item-card ${isModified ? 'highlight-modified' : ''}">
                        <h4>依頼書 #${r.request_no} ${highlight(r.hinmei, tokens)} 
                            ${r.is_handwritten ? '<span class="badge badge-warn" style="margin-left: 8px;">⚠️手書き(要確認)</span>' : ''}
                            ${isModified ? '<span class="badge badge-warn" style="margin-left: 8px; background: #e74c3c;">⚠️修正/関連あり</span>' : ''}
                        </h4>
                        <div class="table-wrap">
                            <table>
                                <tr><th>発行日</th><td>${escapeHtml(r.issue_date)}</td></tr>
                                <tr><th>数量</th><td>${escapeHtml(r.qty)}</td></tr>
                                <tr><th>生地色</th><td>${highlight(r.kiji, tokens)}</td></tr>
                                <tr><th>用途</th><td>${highlight(r.yoto, tokens)}</td></tr>
                                <tr><th>納期</th><td>${escapeHtml(r.noki || r.noki_raw)}</td></tr>
                                <tr><th>出荷先</th><td>${highlight(r.dest, tokens)}</td></tr>
                                <tr><th>規格</th><td><pre style="margin:0;font-family:inherit;white-space:pre-wrap">${highlight(r.spec, tokens)}</pre></td></tr>
                                <tr><th>備考</th><td><pre style="margin:0;font-family:inherit;white-space:pre-wrap">${highlight(r.biko, tokens)}</pre></td></tr>
                            </table>
                        </div>
                        <div class="action-bar">
                            <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(r.previews))}, ${escapeHtml(JSON.stringify(r.file))})'>プレビュー</button>
                            ${r.sp_url ? `<a href="${r.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (r.file ? `<a href="/${r.file.replace(/\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel/画像を開く</a>` : '')}
                            ${r.is_handwritten ? `<button class="btn btn-secondary" onclick="updateHinmei('${escapeHtml(r.request_no)}', '${escapeHtml(r.hinmei)}')">品名を編集</button>` : ''}
                        </div>
                    </div>
                `;
            });
            boxHtml += `</div></div></div>`;
        }"""

new_product_req = """        // Render Requests
        if (group.requests && group.requests.length > 0) {
            // Sort requests descending
            group.requests.sort((a, b) => {
                const numA = parseInt(a.request_no) || 0;
                const numB = parseInt(b.request_no) || 0;
                return numB - numA;
            });
            
            const normalReqs = group.requests.filter(r => !r.is_handwritten);
            const handReqs = group.requests.filter(r => r.is_handwritten);

            if (normalReqs.length > 0) {
                boxHtml += `
                    <div class="section">
                        <div class="section-header" onclick="this.parentElement.classList.toggle('open')">
                            <span>📝 加工依頼書 (${normalReqs.length}件)</span>
                        </div>
                        <div class="section-content">
                            <div class="section-inner">
                `;
                normalReqs.forEach(r => {
                    const isModified = r.file && (r.file.includes('〇') || r.file.includes('×') || r.file.includes('修正'));
                    boxHtml += `
                        <div class="item-card ${isModified ? 'highlight-modified' : ''}">
                            <h4>依頼書 #${r.request_no} ${highlight(r.hinmei, tokens)} 
                                ${isModified ? '<span class="badge badge-warn" style="margin-left: 8px; background: #e74c3c;">⚠️修正/関連あり</span>' : ''}
                            </h4>
                            <div class="table-wrap">
                                <table>
                                    <tr><th>発行日</th><td>${escapeHtml(r.issue_date)}</td></tr>
                                    <tr><th>数量</th><td>${escapeHtml(r.qty)}</td></tr>
                                    <tr><th>生地色</th><td>${highlight(r.kiji, tokens)}</td></tr>
                                    <tr><th>用途</th><td>${highlight(r.yoto, tokens)}</td></tr>
                                    <tr><th>納期</th><td>${escapeHtml(r.noki || r.noki_raw)}</td></tr>
                                    <tr><th>出荷先</th><td>${highlight(r.dest, tokens)}</td></tr>
                                    <tr><th>規格</th><td><pre style="margin:0;font-family:inherit;white-space:pre-wrap">${highlight(r.spec, tokens)}</pre></td></tr>
                                    <tr><th>備考</th><td><pre style="margin:0;font-family:inherit;white-space:pre-wrap">${highlight(r.biko, tokens)}</pre></td></tr>
                                </table>
                            </div>
                            <div class="action-bar">
                                <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(r.previews))}, ${escapeHtml(JSON.stringify(r.file))})'>プレビュー</button>
                                ${r.sp_url ? `<a href="${r.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (r.file ? `<a href="/${r.file.replace(/\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel/画像を開く</a>` : '')}
                            </div>
                        </div>
                    `;
                });
                boxHtml += `</div></div></div>`;
            }

            if (handReqs.length > 0) {
                boxHtml += `
                    <div class="section">
                        <div class="section-header" onclick="this.parentElement.classList.toggle('open')" style="background-color: #fff3cd; color: #856404; border-left-color: #ffeeba;">
                            <span>✍️ 加工依頼書_BOM一体 (${handReqs.length}件)</span>
                        </div>
                        <div class="section-content">
                            <div class="section-inner">
                `;
                handReqs.forEach(r => {
                    const isModified = r.file && (r.file.includes('〇') || r.file.includes('×') || r.file.includes('修正'));
                    let displayHinmei = r.hinmei.replace(/^\[手書き\]\\s*/, '');
                    boxHtml += `
                        <div class="item-card ${isModified ? 'highlight-modified' : ''}" style="border-left: 4px solid #f39c12;">
                            <h4>✍️ 加工依頼書_BOM一体 #${r.request_no} ${highlight(displayHinmei, tokens)} 
                                ${isModified ? '<span class="badge badge-warn" style="margin-left: 8px; background: #e74c3c;">⚠️修正/関連あり</span>' : ''}
                            </h4>
                            <div class="table-wrap">
                                <table>
                                    <tr><th>発行日</th><td>${escapeHtml(r.issue_date)}</td></tr>
                                    <tr><th>数量</th><td>${escapeHtml(r.qty)}</td></tr>
                                    <tr><th>生地色</th><td>${highlight(r.kiji, tokens)}</td></tr>
                                    <tr><th>用途</th><td>${highlight(r.yoto, tokens)}</td></tr>
                                    <tr><th>納期</th><td>${escapeHtml(r.noki || r.noki_raw)}</td></tr>
                                    <tr><th>出荷先</th><td>${highlight(r.dest, tokens)}</td></tr>
                                    <tr><th>規格</th><td><pre style="margin:0;font-family:inherit;white-space:pre-wrap">${highlight(r.spec, tokens)}</pre></td></tr>
                                    <tr><th>備考</th><td><pre style="margin:0;font-family:inherit;white-space:pre-wrap">${highlight(r.biko, tokens)}</pre></td></tr>
                                </table>
                            </div>
                            <div class="action-bar">
                                <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(r.previews))}, ${escapeHtml(JSON.stringify(r.file))})'>プレビュー</button>
                                ${r.sp_url ? `<a href="${r.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (r.file ? `<a href="/${r.file.replace(/\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel/画像を開く</a>` : '')}
                                <button class="btn btn-secondary" onclick="updateHinmei('${escapeHtml(r.request_no)}', '${escapeHtml(r.hinmei)}')">品名を編集</button>
                            </div>
                        </div>
                    `;
                });
                boxHtml += `</div></div></div>`;
            }
        }"""
if old_product_req in content:
    content = content.replace(old_product_req, new_product_req)
else:
    print("Could not find old_product_req!")

# 2. Update renderRequestSearch
old_req_header = """                <div class="group-header">
                    <h2>📄 依頼No: ${highlight(r.request_no, tokens)} ${r.seiban ? `(製番: ${highlight(r.seiban, tokens)})` : ''}</h2>
                    <p style="margin: 0.5rem 0 0 0; font-size: 0.95rem; color: #cbd5e1;">品名: ${highlight(r.hinmei, tokens)} | サイズ: ${escapeHtml(r.size)}</p>
                </div>
                <div class="group-content">
                    <div class="item-card ${isModified ? 'highlight-modified' : ''}" style="border: 2px solid var(--primary); margin-bottom: 1rem;">
                        <h4>加工依頼書: ${escapeHtml(r.file.replace(/\\\\/g, '/').split('/').pop())}
                            ${r.is_handwritten ? '<span class="badge badge-warn" style="margin-left: 8px;">⚠️手書き(要確認)</span>' : ''}
                            ${isModified ? '<span class="badge badge-warn" style="margin-left: 8px; background: #e74c3c;">⚠️修正/関連あり</span>' : ''}
                        </h4>"""

new_req_header = """                <div class="group-header" ${r.is_handwritten ? 'style="background-color: #fff3cd; color: #856404; border-left-color: #ffeeba;"' : ''}>
                    <h2>${r.is_handwritten ? '✍️ 依頼No(BOM一体):' : '📄 依頼No:'} ${highlight(r.request_no, tokens)} ${r.seiban ? `(製番: ${highlight(r.seiban, tokens)})` : ''}</h2>
                    <p style="margin: 0.5rem 0 0 0; font-size: 0.95rem; color: ${r.is_handwritten ? '#856404' : '#cbd5e1'};">品名: ${highlight(r.is_handwritten ? r.hinmei.replace(/^\\[手書き\\]\\s*/, '') : r.hinmei, tokens)} | サイズ: ${escapeHtml(r.size)}</p>
                </div>
                <div class="group-content">
                    <div class="item-card ${isModified ? 'highlight-modified' : ''}" style="border: 2px solid ${r.is_handwritten ? '#f39c12' : 'var(--primary)'}; margin-bottom: 1rem;">
                        <h4>${r.is_handwritten ? '✍️ 加工依頼書_BOM一体' : '加工依頼書'}: ${escapeHtml(r.file.replace(/\\\\/g, '/').split('/').pop())}
                            ${isModified ? '<span class="badge badge-warn" style="margin-left: 8px; background: #e74c3c;">⚠️修正/関連あり</span>' : ''}
                        </h4>"""

if old_req_header in content:
    content = content.replace(old_req_header, new_req_header)
else:
    print("Could not find old_req_header!")

# 3. Update renderGlobalSearch
old_global_req = """    // Render Requests Flat
    if (showReq && allReqs.length > 0) {
        html += `<div class="flat-section"><h3>📄 加工依頼書一覧 (${allReqs.length}件)</h3>`;
        allReqs.forEach(r => {
            const isModified = r.file && (r.file.includes('〇') || r.file.includes('×') || r.file.includes('修正'));
            html += `
                <div class="item-card ${isModified ? 'highlight-modified' : ''}">
                    <h4>${escapeHtml(r.file.replace(/\\\\/g, '/').split('/').pop())}
                        ${r.is_handwritten ? '<span class="badge badge-warn" style="margin-left: 8px;">⚠️手書き(要確認)</span>' : ''}
                        ${isModified ? '<span class="badge badge-warn" style="margin-left: 8px; background: #e74c3c;">⚠️修正/関連あり</span>' : ''}
                    </h4>
                    <p style="margin:0 0 0.5rem 0; font-size:0.85rem; color:var(--text-muted)">
                        依頼No: ${highlight(r.request_no, tokens)} | 製番: ${highlight(r.seiban, tokens)}
                    </p>
                    <div class="table-wrap" style="margin-bottom:0.5rem">
                        <table>
                            <tr><th>品名</th><td>${highlight(r.hinmei, tokens)}</td><th>数量</th><td>${highlight(r.qty, tokens)}</td></tr>
                            <tr><th>生地</th><td>${highlight(r.kiji, tokens)}</td><th>用途</th><td>${highlight(r.yoto, tokens)}</td></tr>
                            <tr><th>仕様</th><td colspan="3">${highlight(r.spec, tokens)}</td></tr>
                            <tr><th>備考</th><td colspan="3">${highlight(r.biko, tokens)}</td></tr>
                        </table>
                    </div>
                    <div class="action-bar">
                        <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(r.previews))}, ${escapeHtml(JSON.stringify(r.file))})'>プレビュー</button>
                        ${r.sp_url ? `<a href="${r.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (r.file ? `<a href="/${r.file.replace(/\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel/画像を開く</a>` : '')}
                        ${r.is_handwritten ? `<button class="btn btn-secondary" onclick="updateHinmei('${escapeHtml(r.request_no)}', '${escapeHtml(r.hinmei)}')">品名を編集</button>` : ''}
                    </div>
                </div>
            `;
        });
        html += `</div>`;
    }"""

new_global_req = """    // Render Requests Flat
    if (showReq && allReqs.length > 0) {
        const normalReqs = allReqs.filter(r => !r.is_handwritten);
        const handReqs = allReqs.filter(r => r.is_handwritten);

        if (normalReqs.length > 0) {
            html += `<div class="flat-section"><h3>📄 加工依頼書一覧 (${normalReqs.length}件)</h3>`;
            normalReqs.forEach(r => {
                const isModified = r.file && (r.file.includes('〇') || r.file.includes('×') || r.file.includes('修正'));
                html += `
                    <div class="item-card ${isModified ? 'highlight-modified' : ''}">
                        <h4>${escapeHtml(r.file.replace(/\\\\/g, '/').split('/').pop())}
                            ${isModified ? '<span class="badge badge-warn" style="margin-left: 8px; background: #e74c3c;">⚠️修正/関連あり</span>' : ''}
                        </h4>
                        <p style="margin:0 0 0.5rem 0; font-size:0.85rem; color:var(--text-muted)">
                            依頼No: ${highlight(r.request_no, tokens)} | 製番: ${highlight(r.seiban, tokens)}
                        </p>
                        <div class="table-wrap" style="margin-bottom:0.5rem">
                            <table>
                                <tr><th>品名</th><td>${highlight(r.hinmei, tokens)}</td><th>数量</th><td>${highlight(r.qty, tokens)}</td></tr>
                                <tr><th>生地</th><td>${highlight(r.kiji, tokens)}</td><th>用途</th><td>${highlight(r.yoto, tokens)}</td></tr>
                                <tr><th>仕様</th><td colspan="3">${highlight(r.spec, tokens)}</td></tr>
                                <tr><th>備考</th><td colspan="3">${highlight(r.biko, tokens)}</td></tr>
                            </table>
                        </div>
                        <div class="action-bar">
                            <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(r.previews))}, ${escapeHtml(JSON.stringify(r.file))})'>プレビュー</button>
                            ${r.sp_url ? `<a href="${r.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (r.file ? `<a href="/${r.file.replace(/\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel/画像を開く</a>` : '')}
                        </div>
                    </div>
                `;
            });
            html += `</div>`;
        }

        if (handReqs.length > 0) {
            html += `<div class="flat-section"><h3>✍️ 加工依頼書_BOM一体 一覧 (${handReqs.length}件)</h3>`;
            handReqs.forEach(r => {
                const isModified = r.file && (r.file.includes('〇') || r.file.includes('×') || r.file.includes('修正'));
                let displayHinmei = r.hinmei.replace(/^\\[手書き\\]\\s*/, '');
                html += `
                    <div class="item-card ${isModified ? 'highlight-modified' : ''}" style="border-left: 4px solid #f39c12;">
                        <h4>✍️ ${escapeHtml(r.file.replace(/\\\\/g, '/').split('/').pop())}
                            ${isModified ? '<span class="badge badge-warn" style="margin-left: 8px; background: #e74c3c;">⚠️修正/関連あり</span>' : ''}
                        </h4>
                        <p style="margin:0 0 0.5rem 0; font-size:0.85rem; color:var(--text-muted)">
                            依頼No: ${highlight(r.request_no, tokens)} | 製番: ${highlight(r.seiban, tokens)}
                        </p>
                        <div class="table-wrap" style="margin-bottom:0.5rem">
                            <table>
                                <tr><th>品名</th><td>${highlight(displayHinmei, tokens)}</td><th>数量</th><td>${highlight(r.qty, tokens)}</td></tr>
                                <tr><th>生地</th><td>${highlight(r.kiji, tokens)}</td><th>用途</th><td>${highlight(r.yoto, tokens)}</td></tr>
                                <tr><th>仕様</th><td colspan="3">${highlight(r.spec, tokens)}</td></tr>
                                <tr><th>備考</th><td colspan="3">${highlight(r.biko, tokens)}</td></tr>
                            </table>
                        </div>
                        <div class="action-bar">
                            <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(r.previews))}, ${escapeHtml(JSON.stringify(r.file))})'>プレビュー</button>
                            ${r.sp_url ? `<a href="${r.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (r.file ? `<a href="/${r.file.replace(/\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel/画像を開く</a>` : '')}
                            <button class="btn btn-secondary" onclick="updateHinmei('${escapeHtml(r.request_no)}', '${escapeHtml(r.hinmei)}')">品名を編集</button>
                        </div>
                    </div>
                `;
            });
            html += `</div>`;
        }
    }"""

if old_global_req in content:
    content = content.replace(old_global_req, new_global_req)
else:
    print("Could not find old_global_req!")

with open('static/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch complete.")
