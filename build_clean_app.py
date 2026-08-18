import re

with open('static/app_raw.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove the old performSearch
start = text.find('async function performSearch()')
end = text.find('window.openPreview = function')
if start == -1 or end == -1:
    print('Could not find performSearch bounds in app_raw.js')
    exit(1)

# Extract everything before performSearch
head = text[:start]
# Extract everything after performSearch
tail = text[end:]

new_perform_search = """
let GLOBAL_DATA = [];
async function loadData() {
    try {
        const res = await fetch('/data.json');
        GLOBAL_DATA = await res.json();
        performSearch();
    } catch (e) {
        console.error('Failed to load data.json', e);
    }
}
document.addEventListener('DOMContentLoaded', loadData);

function createTag(text, type) {
    if (!text) return '';
    return `<span class="tag" onclick="triggerTagSearch('${text.replace(/'/g, "\\\\'")}', '${type || ''}')">${escapeHtml(text)}</span>`;
}

async function performSearch() {
    const seiban = document.getElementById('searchSeiban').value.trim();
    const req = document.getElementById('searchReq').value.trim();
    const product = document.getElementById('searchProduct').value.trim();
    const partInputs = Array.from(document.querySelectorAll('.searchPartInput')).map(i => i.value.trim()).filter(v => v !== '');
    const part = partInputs.join(' ');
    const company = document.getElementById('searchCompany').value.trim();
    const q = document.getElementById('searchInput').value.trim();
    
    const normalize = (text) => {
        if (!text) return "";
        let t = String(text).toLowerCase();
        t = t.replace(/[Ａ-Ｚａ-ｚ０-９]/g, function(s) {
            return String.fromCharCode(s.charCodeAt(0) - 0xFEE0);
        });
        return t;
    };

    // Split keywords
    const search_seiban = normalize(seiban);
    const search_req = normalize(req);
    const search_product = normalize(product);
    const search_part = part.split(/\s+/).map(normalize).filter(v=>v);
    const search_company = normalize(company);
    const search_q = q.split(/\s+/).map(normalize).filter(v=>v);
    
    // Global filters
    const showBom = document.getElementById('filterBom').checked;
    const showReq = document.getElementById('filterReq').checked;
    const showInsp = document.getElementById('filterInsp').checked;
    const showPhoto = document.getElementById('filterPhoto').checked;
    const showDrawing = document.getElementById('filterDrawing').checked;
    
    const resultsContainer = document.getElementById('results');
    const statsContainer = document.getElementById('stats');
    resultsContainer.innerHTML = '<div style="text-align:center; padding: 2rem; color: #666;">検索中...</div>';
    statsContainer.textContent = '';
    
    // Delay to allow UI to render "検索中..."
    await new Promise(r => setTimeout(r, 50));
    
    let filteredGroups = [];
    let totalBoms = 0, totalReqs = 0, totalInsps = 0, totalPhotos = 0, totalDrawings = 0;
    
    for (let g of GLOBAL_DATA) {
        if (!g.boms.length && !g.requests.length && !g.inspections.length && !g.photos.length && !g.drawings.length) continue;
        
        let match_seiban = true;
        let match_req = true;
        let match_product = true;
        let match_part = true;
        let match_company = true;
        let match_general = true;
        
        if (search_seiban && !normalize(g._search_seiban || '').includes(search_seiban)) match_seiban = false;
        if (search_req && !normalize(g._search_req || '').includes(search_req)) match_req = false;
        if (search_product && !normalize(g._search_product || '').includes(search_product)) match_product = false;
        if (search_part.length > 0) {
            for (let token of search_part) {
                if (!normalize(g._search_part || '').includes(token)) {
                    match_part = false; break;
                }
            }
        }
        if (search_company && !normalize(g._search_company || '').includes(search_company)) match_company = false;
        if (search_q.length > 0) {
            for (let token of search_q) {
                if (!normalize(g._search_text || '').includes(token)) {
                    match_general = false; break;
                }
            }
        }
        
        if (match_seiban && match_req && match_product && match_part && match_company && match_general) {
            let g_out = JSON.parse(JSON.stringify(g));
            if (search_req && g_out.requests) {
                g_out.requests = g_out.requests.filter(r => normalize(r.request_no || '').includes(search_req) || normalize(r.hinmei || '').includes(search_req));
            }
            if (search_seiban && g_out.seibans) {
                if (g_out.seibans.some(s => normalize(s).includes(search_seiban))) {
                    // Keep
                } else {
                    if (g_out.boms) g_out.boms = g_out.boms.filter(b => normalize(b.seiban || '').includes(search_seiban));
                    if (g_out.requests) g_out.requests = g_out.requests.filter(r => normalize(r.seiban || '').includes(search_seiban));
                }
            }
            filteredGroups.push(g_out);
            totalBoms += g_out.boms.length;
            totalReqs += g_out.requests.length;
            totalInsps += g_out.inspections.length;
            totalPhotos += g_out.photos.length;
            totalDrawings += g_out.drawings.length;
        }
    }
    
    // Sort by key
    filteredGroups.sort((a,b) => {
        if (a.new_part_no === '未分類') return 1;
        if (b.new_part_no === '未分類') return -1;
        return (a.new_part_no || '').localeCompare(b.new_part_no || '');
    });
    
    const isFlatView = (currentTab !== 'product');
    if (isFlatView) {
        renderFlat(filteredGroups, showBom, showReq, showInsp, showPhoto, showDrawing, resultsContainer, statsContainer);
    } else {
        renderGroups(filteredGroups, showBom, showReq, showInsp, showPhoto, showDrawing, resultsContainer, statsContainer);
    }
}

function renderGroups(groups, showBom, showReq, showInsp, showPhoto, showDrawing, resultsContainer, statsContainer) {
    let html = '';
    
    let displayGroups = groups;
    if (groups.length > 50) {
        displayGroups = groups.slice(0, 50);
        statsContainer.textContent = `${groups.length} 製品群が見つかりました (検索結果が多すぎるため上位50件のみ表示)`;
    } else {
        statsContainer.textContent = `${groups.length} 製品群が見つかりました`;
    }
    
    displayGroups.forEach(group => {
        const isUnclassified = group.new_part_no === '未分類';
        const pCode = group.product ? group.product.product_code : '';
        const pName = group.product ? group.product.name : '';
        const titleText = isUnclassified ? '未分類の書類' : `${escapeHtml(pCode)} ${escapeHtml(pName)}`;
        
        const boms = showBom ? (group.boms || []) : [];
        const reqs = showReq ? (group.requests || []) : [];
        const insps = showInsp ? (group.inspections || []) : [];
        const photos = showPhoto ? (group.photos || []) : [];
        const drawings = showDrawing ? (group.drawings || []) : [];
        
        if (boms.length === 0 && reqs.length === 0 && insps.length === 0 && photos.length === 0 && drawings.length === 0) return;
        
        const normalReqs = reqs.filter(r => !r.is_handwritten);
        const handReqs = reqs.filter(r => r.is_handwritten);
        
        html += `
            <div class="card">
                <div class="card-header">
                    <h2>
                        ${isUnclassified ? '<span class="badge badge-unclassified">未分類</span>' : ''}
                        ${escapeHtml(titleText)}
                        ${(group.product && group.product.name === '未登録製品') ? `<button class="btn btn-secondary" style="margin-left: 1rem; padding: 2px 8px; font-size: 0.85rem;" onclick="registerProductName('${escapeHtml(pCode).replace(/'/g, "\\\\\\\\'")}')">製品名を登録する</button>` : ''}
                    </h2>
                    ${group.seibans && group.seibans.length ? group.seibans.map(s => `<span class="badge badge-seiban">製番: ${escapeHtml(s)}</span>`).join('') : ''}
                </div>
                <div class="card-content">
        `;
        
        if (boms.length > 0) {
            html += `<div class="sub-section"><h3>📦 BOM (${boms.length}件)</h3>`;
            boms.forEach(b => {
                let compsHtml = '';
                if (b.components) {
                    compsHtml = '<div class="table-wrap" style="margin-bottom:0.5rem"><table><tr><th>役割</th><th>部品番号</th><th>仕様メモ</th></tr>';
                    if (Array.isArray(b.components)) {
                        b.components.forEach(c => {
                            compsHtml += `<tr>
                                <td>${escapeHtml(c.role)}</td>
                                <td>${createTag(c.part_no, 'part')}</td>
                                <td>${escapeHtml(c.note)}</td>
                            </tr>`;
                        });
                    } else {
                        compsHtml += `<tr><td colspan="3"><pre style="white-space:pre-wrap; font-size:11px; color:#666;">${escapeHtml(String(b.components))}</pre></td></tr>`;
                    }
                    compsHtml += `</table></div>`;
                }
                
                html += `
                    <div class="item-card">
                        <h4>${escapeHtml(b.file.replace(/\\\\\\\\/g, '/').split('/').pop())}</h4>
                        <p style="margin:0 0 0.5rem 0; font-size:0.85rem; color:var(--text-muted)">
                            製番: ${escapeHtml(b.seiban)}
                        </p>
                        ${compsHtml}
                        <div class="action-bar">
                            <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(b.previews))}, ${escapeHtml(JSON.stringify(b.file))})'>プレビュー</button>
                            ${b.sp_url ? `<a href="${b.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (b.file ? `<a href="/${b.file.replace(/\\\\\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excelを開く</a>` : '')}
                        </div>
                    </div>
                `;
            });
            html += `</div>`;
        }
        
        if (normalReqs.length > 0) {
            html += `<div class="sub-section"><h3>📄 加工依頼書 (${normalReqs.length}件)</h3>`;
            normalReqs.forEach(r => {
                const isModified = r.file && (r.file.includes('変更') || r.file.includes('追加') || r.file.includes('修正'));
                html += `
                    <div class="item-card ${isModified ? 'highlight-modified' : ''}">
                        <h4>${escapeHtml(r.file.replace(/\\\\\\\\/g, '/').split('/').pop())}
                            ${isModified ? '<span class="badge badge-warn" style="margin-left: 8px; background: #e74c3c;">⚠️修正/関連あり</span>' : ''}
                        </h4>
                        <p style="margin:0 0 0.5rem 0; font-size:0.85rem; color:var(--text-muted)">
                            依頼No: ${escapeHtml(r.request_no)} | 製番: ${escapeHtml(r.seiban)}
                        </p>
                        <div class="table-wrap" style="margin-bottom:0.5rem">
                            <table>
                                <tr><th>品名</th><td>${escapeHtml(r.hinmei)}</td><th>数量</th><td>${escapeHtml(r.qty)}</td></tr>
                                <tr><th>生地</th><td>${escapeHtml(r.kiji)}</td><th>用途</th><td>${escapeHtml(r.yoto)}</td></tr>
                                <tr><th>仕様</th><td colspan="3">${escapeHtml(r.spec)}</td></tr>
                                <tr><th>備考</th><td colspan="3">${escapeHtml(r.biko)}</td></tr>
                            </table>
                        </div>
                        <div class="action-bar">
                            <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(r.previews))}, ${escapeHtml(JSON.stringify(r.file))})'>プレビュー</button>
                            ${r.sp_url ? `<a href="${r.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (r.file ? `<a href="/${r.file.replace(/\\\\\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel/画像を開く</a>` : '')}
                        </div>
                    </div>
                `;
            });
            html += `</div>`;
        }
        
        if (handReqs.length > 0) {
            html += `<div class="sub-section"><h3>✍️ 加工依頼書_BOM一体 (${handReqs.length}件)</h3>`;
            handReqs.forEach(r => {
                const isModified = r.file && (r.file.includes('変更') || r.file.includes('追加') || r.file.includes('修正'));
                let displayHinmei = r.hinmei.replace(/^\[手書き\]\\s*/, '');
                html += `
                    <div class="item-card ${isModified ? 'highlight-modified' : ''}" style="border-left: 4px solid #f39c12;">
                        <h4>✍️ ${escapeHtml(r.file.replace(/\\\\\\\\/g, '/').split('/').pop())}
                            ${isModified ? '<span class="badge badge-warn" style="margin-left: 8px; background: #e74c3c;">⚠️修正/関連あり</span>' : ''}
                        </h4>
                        <p style="margin:0 0 0.5rem 0; font-size:0.85rem; color:var(--text-muted)">
                            依頼No: ${escapeHtml(r.request_no)} | 製番: ${escapeHtml(r.seiban)}
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
                                                <td>${escapeHtml(c.role)}</td>
                                                <td>${createTag(c.part_no, 'part')}</td>
                                                <td>${escapeHtml(c.note)}</td>
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
                            ${r.sp_url ? `<a href="${r.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (r.file ? `<a href="/${r.file.replace(/\\\\\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel/画像を開く</a>` : '')}
                            <button class="btn btn-secondary" onclick="updateHinmei('${escapeHtml(r.request_no)}', '${escapeHtml(r.hinmei)}')">品名を編集</button>
                        </div>
                    </div>
                `;
            });
            html += `</div>`;
        }

        if (insps.length > 0) {
            html += `<div class="sub-section"><h3>📋 関連検査証 (${insps.length}件)</h3><div style="display:flex; flex-wrap:wrap; gap:0.5rem">`;
            insps.forEach(i => {
                html += `<div class="item-card" style="margin:0; flex:1; min-width:200px">
                    <p style="margin:0 0 0.5rem 0; font-size:0.85rem">${escapeHtml(i.file_path.replace(/\\\\\\\\/g, '/').split('/').pop())}</p>
                    <div class="action-bar">
                        <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(i.previews))}, ${escapeHtml(JSON.stringify(i.file_path))})'>プレビュー</button>
                        ${i.sp_url ? `<a href="${i.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (i.file_path ? `<a href="/${i.file_path.replace(/\\\\\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">開く</a>` : '')}
                    </div>
                </div>`;
            });
            html += `</div></div>`;
        }
        
        if (photos.length > 0) {
            html += `<div class="sub-section"><h3>📸 関連写真・その他 (${photos.length}件)</h3><div style="display:flex; flex-wrap:wrap; gap:0.5rem">`;
            photos.forEach(p => {
                html += `<div class="item-card" style="margin:0; flex:1; min-width:200px">
                    <p style="margin:0 0 0.5rem 0; font-size:0.85rem">${escapeHtml(p.file_path.replace(/\\\\\\\\/g, '/').split('/').pop())}</p>
                    <img src="/${p.file_path.replace(/\\\\\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}?t=${Date.now()}" style="max-width:100%; border-radius:4px; margin-bottom:0.5rem">
                    <div class="action-bar">
                        ${p.file_path ? `<a href="/${p.file_path.replace(/\\\\\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">開く</a>` : ''}
                    </div>
                </div>`;
            });
            html += `</div></div>`;
        }
        
        if (drawings.length > 0) {
            html += `<div class="sub-section"><h3>📐 関連図面 (${drawings.length}件)</h3><div style="display:flex; flex-wrap:wrap; gap:0.5rem">`;
            drawings.forEach(d => {
                html += `<div class="item-card" style="margin:0; flex:1; min-width:200px">
                    <p style="margin:0 0 0.5rem 0; font-size:0.85rem">${escapeHtml(d.file_path.replace(/\\\\\\\\/g, '/').split('/').pop())}</p>
                    <div class="action-bar">
                        ${d.previews && d.previews.length > 0 && d.previews[0] !== 'previews/dummy_0.png' ? `<button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(d.previews))}, ${escapeHtml(JSON.stringify(d.file_path))})'>プレビュー</button>` : ''}
                        ${d.file_path ? `<a href="/${d.file_path.replace(/\\\\\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">ダウンロード / 開く</a>` : ''}
                    </div>
                </div>`;
            });
            html += `</div></div>`;
        }

        html += `</div></div>`;
    });
    
    if (html === '') {
        html = '<div class="empty-state">該当するデータがありません</div>';
    }
    resultsContainer.innerHTML = html;
}

function renderFlat(groups, showBom, showReq, showInsp, showPhoto, showDrawing, resultsContainer, statsContainer) {
    let html = '';
    
    let allBoms = [];
    let allReqs = [];
    let allInsps = [];
    let allPhotos = [];
    let allDrawings = [];
    
    // Build flat arrays
    groups.forEach(group => {
        if (group.boms) {
            group.boms.forEach(b => {
                b._product = group.product;
                allBoms.push(b);
            });
        }
        if (group.requests) {
            group.requests.forEach(r => {
                r._product = group.product;
                allReqs.push(r);
            });
        }
        if (group.inspections) {
            group.inspections.forEach(i => {
                i._product = group.product;
                allInsps.push(i);
            });
        }
        if (group.photos) {
            group.photos.forEach(p => {
                p._product = group.product;
                allPhotos.push(p);
            });
        }
        if (group.drawings) {
            group.drawings.forEach(d => {
                d._product = group.product;
                allDrawings.push(d);
            });
        }
    });
    
    const normalReqs = allReqs.filter(r => !r.is_handwritten);
    const handReqs = allReqs.filter(r => r.is_handwritten);
    
    let totalFound = 0;
    if (showBom) totalFound += allBoms.length;
    if (showReq) totalFound += allReqs.length;
    if (showInsp) totalFound += allInsps.length;
    if (showPhoto) totalFound += allPhotos.length;
    if (showDrawing) totalFound += allDrawings.length;
    
    if (totalFound > 100) {
        if (showBom) allBoms = allBoms.slice(0, 100);
        if (showReq) {
            const allowed = 100 - allBoms.length;
            const toKeep = allReqs.slice(0, allowed);
            // Re-filter for display
            normalReqs.length = 0;
            handReqs.length = 0;
            toKeep.forEach(r => {
                if(r.is_handwritten) handReqs.push(r);
                else normalReqs.push(r);
            });
        }
        if (showInsp) allInsps = allInsps.slice(0, Math.max(0, 100 - allBoms.length - allReqs.length));
        if (showPhoto) allPhotos = allPhotos.slice(0, Math.max(0, 100 - allBoms.length - allReqs.length - allInsps.length));
        if (showDrawing) allDrawings = allDrawings.slice(0, Math.max(0, 100 - allBoms.length - allReqs.length - allInsps.length - allPhotos.length));
    }
    
    statsContainer.textContent = `${totalFound}件見つかりました${totalFound > 100 ? ' (最大100件を表示)' : ''}`;
    
    if (showBom && allBoms.length > 0) {
        html += `<div class="flat-section"><h3>📦 BOM一覧 (${allBoms.length}件)</h3>`;
        allBoms.forEach(b => {
            let compsHtml = '';
            if (b.components) {
                compsHtml = '<div class="table-wrap" style="margin-bottom:0.5rem"><table><tr><th>役割</th><th>部品番号</th><th>仕様メモ</th></tr>';
                if (Array.isArray(b.components)) {
                    b.components.forEach(c => {
                        compsHtml += `<tr>
                            <td>${escapeHtml(c.role)}</td>
                            <td>${createTag(c.part_no, 'part')}</td>
                            <td>${escapeHtml(c.note)}</td>
                        </tr>`;
                    });
                } else {
                    compsHtml += `<tr><td colspan="3"><pre style="white-space:pre-wrap; font-size:11px; color:#666;">${escapeHtml(String(b.components))}</pre></td></tr>`;
                }
                compsHtml += `</table></div>`;
            }
            html += `
                <div class="item-card">
                    <h4>${escapeHtml(b.file.replace(/\\\\\\\\/g, '/').split('/').pop())}</h4>
                    <p style="margin:0 0 0.5rem 0; font-size:0.85rem; color:var(--text-muted)">
                        製番: ${escapeHtml(b.seiban)} | 品名: ${escapeHtml(b._product && b._product.name)}
                    </p>
                    ${compsHtml}
                    <div class="action-bar">
                        <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(b.previews))}, ${escapeHtml(JSON.stringify(b.file))})'>プレビュー</button>
                        ${b.sp_url ? `<a href="${b.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (b.file ? `<a href="/${b.file.replace(/\\\\\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excelを開く</a>` : '')}
                    </div>
                </div>
            `;
        });
        html += `</div>`;
    }

    if (showReq && normalReqs.length > 0) {
        html += `<div class="flat-section"><h3>📄 加工依頼書一覧 (${normalReqs.length}件)</h3>`;
        normalReqs.forEach(r => {
            const isModified = r.file && (r.file.includes('変更') || r.file.includes('追加') || r.file.includes('修正'));
            html += `
                <div class="item-card ${isModified ? 'highlight-modified' : ''}">
                    <h4>${escapeHtml(r.file.replace(/\\\\\\\\/g, '/').split('/').pop())}
                        ${isModified ? '<span class="badge badge-warn" style="margin-left: 8px; background: #e74c3c;">⚠️修正/関連あり</span>' : ''}
                    </h4>
                    <p style="margin:0 0 0.5rem 0; font-size:0.85rem; color:var(--text-muted)">
                        依頼No: ${escapeHtml(r.request_no)} | 製番: ${escapeHtml(r.seiban)}
                    </p>
                    <div class="table-wrap" style="margin-bottom:0.5rem">
                        <table>
                            <tr><th>品名</th><td>${escapeHtml(r.hinmei)}</td><th>数量</th><td>${escapeHtml(r.qty)}</td></tr>
                            <tr><th>生地</th><td>${escapeHtml(r.kiji)}</td><th>用途</th><td>${escapeHtml(r.yoto)}</td></tr>
                            <tr><th>仕様</th><td colspan="3">${escapeHtml(r.spec)}</td></tr>
                            <tr><th>備考</th><td colspan="3">${escapeHtml(r.biko)}</td></tr>
                        </table>
                    </div>
                    <div class="action-bar">
                        <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(r.previews))}, ${escapeHtml(JSON.stringify(r.file))})'>プレビュー</button>
                        ${r.sp_url ? `<a href="${r.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (r.file ? `<a href="/${r.file.replace(/\\\\\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel/画像を開く</a>` : '')}
                    </div>
                </div>
            `;
        });
        html += `</div>`;
    }
    
    if (showReq && handReqs.length > 0) {
        html += `<div class="flat-section"><h3>✍️ 加工依頼書_BOM一体一覧 (${handReqs.length}件)</h3>`;
        handReqs.forEach(r => {
            const isModified = r.file && (r.file.includes('変更') || r.file.includes('追加') || r.file.includes('修正'));
            let displayHinmei = r.hinmei.replace(/^\[手書き\]\\s*/, '');
            html += `
                <div class="item-card ${isModified ? 'highlight-modified' : ''}" style="border-left: 4px solid #f39c12;">
                    <h4>✍️ ${escapeHtml(r.file.replace(/\\\\\\\\/g, '/').split('/').pop())}
                        ${isModified ? '<span class="badge badge-warn" style="margin-left: 8px; background: #e74c3c;">⚠️修正/関連あり</span>' : ''}
                    </h4>
                    <p style="margin:0 0 0.5rem 0; font-size:0.85rem; color:var(--text-muted)">
                        依頼No: ${escapeHtml(r.request_no)} | 製番: ${escapeHtml(r.seiban)}
                    </p>
                    <div class="table-wrap">
                        ${(() => {
                            // Fix: look up components from allBoms because group.boms is not available here!
                            const matchingBoms = allBoms.filter(b => b.ref_requests && b.ref_requests.includes(r.request_no));
                            if (matchingBoms.length > 0 && matchingBoms[0].components) {
                                const b = matchingBoms[0];
                                let compsHtml = '<table><tr><th>役割</th><th>部品番号</th><th>仕様メモ</th></tr>';
                                if (Array.isArray(b.components)) {
                                    b.components.forEach(c => {
                                        compsHtml += `<tr>
                                            <td>${escapeHtml(c.role)}</td>
                                            <td>${createTag(c.part_no, 'part')}</td>
                                            <td>${escapeHtml(c.note)}</td>
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
                        ${r.sp_url ? `<a href="${r.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (r.file ? `<a href="/${r.file.replace(/\\\\\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel/画像を開く</a>` : '')}
                        <button class="btn btn-secondary" onclick="updateHinmei('${escapeHtml(r.request_no)}', '${escapeHtml(r.hinmei)}')">品名を編集</button>
                    </div>
                </div>
            `;
        });
        html += `</div>`;
    }

    if (showInsp && allInsps.length > 0) {
        html += `<div class="flat-section"><h3>📋 検査証一覧 (${allInsps.length}件)</h3><div style="display:flex; flex-wrap:wrap; gap:1rem">`;
        allInsps.forEach(i => {
            html += `
                <div class="item-card" style="flex:1; min-width:300px">
                    <h4>${escapeHtml(i.file_path.replace(/\\\\\\\\/g, '/').split('/').pop())}</h4>
                    <div class="action-bar">
                        <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(i.previews))}, ${escapeHtml(JSON.stringify(i.file_path))})'>プレビュー</button>
                        ${i.sp_url ? `<a href="${i.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (i.file_path ? `<a href="/${i.file_path.replace(/\\\\\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">開く</a>` : '')}
                    </div>
                </div>
            `;
        });
        html += `</div></div>`;
    }

    if (showPhoto && allPhotos.length > 0) {
        html += `<div class="flat-section"><h3>📸 写真・その他一覧 (${allPhotos.length}件)</h3><div style="display:flex; flex-wrap:wrap; gap:1rem">`;
        allPhotos.forEach(p => {
            const pName = p._product && p._product.name ? ` (${p._product.name})` : '';
            const pCode = p._product ? p._product.product_code : '未分類';
            html += `
                <div class="item-card" style="flex:1; min-width:300px">
                    <h4>${escapeHtml(p.file_path.replace(/\\\\\\\\/g, '/').split('/').pop())}</h4>
                    <p style="font-size:0.85rem; color:var(--text-muted); margin: 0 0 0.5rem 0;">関連製品: ${escapeHtml(pCode)}${escapeHtml(pName)}</p>
                    <img src="/${p.file_path.replace(/\\\\\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}?t=${Date.now()}" style="max-width:100%; border-radius:4px; margin-bottom:0.5rem">
                    <div class="action-bar">
                        ${p.file_path ? `<a href="/${p.file_path.replace(/\\\\\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">開く</a>` : ''}
                    </div>
                </div>
            `;
        });
        html += `</div></div>`;
    }
    
    if (showDrawing && allDrawings.length > 0) {
        html += `<div class="flat-section"><h3>📐 図面一覧 (${allDrawings.length}件)</h3><div style="display:flex; flex-wrap:wrap; gap:1rem">`;
        allDrawings.forEach(d => {
            const pName = d._product && d._product.name ? ` (${d._product.name})` : '';
            const pCode = d._product ? d._product.product_code : '未分類';
            html += `
                <div class="item-card" style="flex:1; min-width:250px">
                    <h4>${escapeHtml(d.file_path.replace(/\\\\\\\\/g, '/').split('/').pop())}</h4>
                    <p style="font-size:0.85rem; color:var(--text-muted); margin: 0 0 0.5rem 0;">関連製品: ${escapeHtml(pCode)}${escapeHtml(pName)}</p>
                    <div class="action-bar">
                        ${d.previews && d.previews.length > 0 && d.previews[0] !== 'previews/dummy_0.png' ? `<button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(d.previews))}, ${escapeHtml(JSON.stringify(d.file_path))})'>プレビュー</button>` : ''}
                        ${d.file_path ? `<a href="/${d.file_path.replace(/\\\\\\\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">ダウンロード / 開く</a>` : ''}
                    </div>
                </div>
            `;
        });
        html += `</div></div>`;
    }

    if (html === '') {
        html = '<div class="empty-state">チェックされた項目に該当するデータがありません</div>';
    }
    
    if (totalFound > 100) {
        html += '<div style="text-align:center; padding:1.5rem; margin-top:1rem; border-top:1px solid var(--border); color:var(--text-muted);">検索結果が多すぎるため、上位100件のみを表示しています。条件を絞り込んでください。</div>';
    }
    
    resultsContainer.innerHTML = html;
}
"""

with open('static/app.js', 'w', encoding='utf-8-sig') as f:
    f.write(head + new_perform_search + "\n\n" + tail)

print("Successfully rebuilt app.js")
