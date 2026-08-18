import re
import codecs

with codecs.open('static/app.js', 'r', 'utf-8') as f:
    content = f.read()

start_idx = content.find('// Render Requests Flat')
if start_idx == -1:
    print("Could not find '// Render Requests Flat'")
    exit(1)

end_idx = content.find('// Render Inspections', start_idx)
if end_idx == -1:
    print("Could not find '// Render Inspections'")
    exit(1)

new_global_req = """    // Render Requests Flat
    if (showReq && allReqs.length > 0) {
        const normalReqs = allReqs.filter(r => !r.is_handwritten);
        const handReqs = allReqs.filter(r => r.is_handwritten);

        if (normalReqs.length > 0) {
            html += `<div class="flat-section"><h3>📄 加工依頼書一覧 (${normalReqs.length}件)</h3>`;
            normalReqs.forEach(r => {
                const isModified = r.file && (r.file.includes('変更') || r.file.includes('追加') || r.file.includes('修正'));
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
            html += `<div class="flat-section"><h3>✍️ 加工依頼書_BOM一体一覧 (${handReqs.length}件)</h3>`;
            handReqs.forEach(r => {
                const isModified = r.file && (r.file.includes('変更') || r.file.includes('追加') || r.file.includes('修正'));
                let displayHinmei = r.hinmei.replace(/^\\[手書き\\]\\s*/, '');
                html += `
                    <div class="item-card ${isModified ? 'highlight-modified' : ''}" style="border-left: 4px solid #f39c12;">
                        <h4>✍️ ${escapeHtml(r.file.replace(/\\\\/g, '/').split('/').pop())}
                            ${isModified ? '<span class="badge badge-warn" style="margin-left: 8px; background: #e74c3c;">⚠️修正/関連あり</span>' : ''}
                        </h4>
                        <p style="margin:0 0 0.5rem 0; font-size:0.85rem; color:var(--text-muted)">
                            依頼No: ${highlight(r.request_no, tokens)} | 製番: ${highlight(r.seiban, tokens)}
                        </p>
                        
                            <div class="table-wrap">
                                ${(() => {
                                    const matchingBoms = (group.boms || []).filter(b => b.ref_requests && b.ref_requests.includes(r.request_no));
                                    if (matchingBoms.length > 0 && matchingBoms[0].components) {
                                        const b = matchingBoms[0];
                                        let compsHtml = '<table><tr><th>役割</th><th>部品番号</th><th>仕様メモ</th></tr>';
                                        if (Array.isArray(b.components)) {
                                            b.components.forEach(c => {
                                                compsHtml += `<tr>
                                                    <td>${highlight(c.role, tokens)}</td>
                                                    <td>${createTag(c.part_no, 'part')}</td>
                                                    <td>${highlight(c.note, tokens)}</td>
                                                </tr>`;
                                            });
                                        } else {
                                            compsHtml += `<tr><td colspan="3"><pre style="white-space:pre-wrap; font-size:11px; color:#666;">${escapeHtml(String(b.components))}</pre></td></tr>`;
                                        }
                                        compsHtml += '</table>';
                                        return compsHtml;
                                    } else {
                                        return '<div style="padding:8px;color:#666;">部品情報が見つかりません</div>';
                                    }
                                })()}
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
    }
"""

content = content[:start_idx] + new_global_req + content[end_idx:]

with codecs.open('static/app.js', 'w', 'utf-8') as f:
    f.write(content)

print("Patched app.js successfully!")
