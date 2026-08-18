async function performSearch() {
    const seiban = document.getElementById('searchSeiban').value.trim();
    const req = document.getElementById('searchReq').value.trim();
    const product = document.getElementById('searchProduct').value.trim();
    const partInputs = Array.from(document.querySelectorAll('.searchPartInput')).map(i => i.value.trim()).filter(v => v !== '');
    const part = partInputs.join(' ');
    const company = document.getElementById('searchCompany').value.trim();
    const q = document.getElementById('searchInput').value.trim();

    if (!q && !seiban && !req && !product && !part && !company) {
        document.getElementById('results').innerHTML = '<div class="empty-state">検索条件を入力してください</div>';
        return;
    }

    const params = new URLSearchParams();
    if(q) params.append('q', q);
    if(seiban) params.append('seiban', seiban);
    if(req) params.append('req_no', req);
    if(product) params.append('product', product);
    if(part) params.append('part_no', part);
    if(company) params.append('company', company);

    try {
        const response = await fetch(`/api/search?${params.toString()}`);
        const data = await response.json();
        lastGroups = data.results;
        const state = { q, seiban, req_no: req, product, part_no: part, company: company };
        renderResults(data.results, state);
        if (data.has_more) {
            resultsContainer.insertAdjacentHTML('beforeend', '<div style="text-align:center; padding:1.5rem; margin-top:1rem; border-top:1px solid var(--border); color:var(--text-muted);">ℹ️ 結果が多すぎるため、上位100件のみを表示しています。さらに条件を絞り込んでください。</div>');
        }
    } catch (err) {
        console.error("Search error:", err);
        resultsContainer.innerHTML = '<div style="color:var(--danger)">検索エラーが発生しました</div>';
    }
}

// Generate tag chips for recursive search
function createTag(text, type) {
    if (!text) return '';
    return `<span class="tag" onclick="triggerTagSearch('${text.replace(/'/g, "\\'")}', '${type || ''}')">${escapeHtml(text)}</span>`;
}

window.triggerTagSearch = function(keyword, type) {
    if (type === 'part') {
        const inputs = document.querySelectorAll('.searchPartInput');
        let filled = false;
        for (let i = 0; i < inputs.length; i++) {
            if (!inputs[i].value) {
                inputs[i].value = keyword;
                filled = true;
                break;
            } else if (inputs[i].value === keyword) {
                filled = true;
                break;
            }
        }
        if (!filled) {
            addPartInput(keyword);
        }
        
        document.getElementById('searchInput').value = '';
        document.getElementById('searchSeiban').value = '';
        document.getElementById('searchReq').value = '';
        document.getElementById('searchProduct').value = '';
        document.getElementById('searchCompany').value = '';
    } else {
        document.getElementById('searchInput').value = '';
        document.getElementById('searchSeiban').value = '';
        document.getElementById('searchReq').value = '';
        document.getElementById('searchProduct').value = '';
        document.getElementById('searchCompany').value = '';
        
        const list = document.getElementById('partInputsList');
        if (list) {
            list.innerHTML = `
                <div class="part-input-row" style="display: flex; gap: 4px; flex: 1;">
                    <input type="text" class="searchPartInput" placeholder="例: IF000-304" style="width: 100%;">
                </div>
            `;
            document.querySelector('.searchPartInput').addEventListener('input', () => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(performSearch, 300);
            });
            document.getElementById('addPartBtn').disabled = false;
        }
        
        if (keyword.startsWith('#')) {
            document.getElementById('searchReq').value = keyword.substring(1);
        } else {
            document.getElementById('searchInput').value = keyword;
        }
        performSearch();
    }
};

// Render the UI
function renderResults(groups, state) {
    let tokens = Object.values(state).filter(x => x).join(' ').split(/\s+/).filter(x => x);
    
    if (!groups || groups.length === 0) {
        statsContainer.textContent = '該当するデータがありません';
        resultsContainer.innerHTML = '';
        return;
    }

    if (currentTab === 'product') {
        renderProductSearch(groups, tokens);
    } else if (currentTab === 'request') {
        renderRequestSearch(groups, tokens);
    } else {
        renderGlobalSearch(groups, tokens, state);
    }
}

function renderProductSearch(groups, tokens) {
    let html = '';
    statsContainer.textContent = `${groups.length} 製品箱が見つかりました`;

    groups.forEach(group => {
        const p = group.product || {};
        const isUnclassified = !p.product_code;
        const pCode = p.product_code || '未分類';
        let titleText = pCode;
        if (p.name && p.name !== '未登録部品' && p.name !== '未登録製品(依頼書)') {
            titleText = p.name;
            if (!titleText.includes(pCode)) {
                titleText = `${pCode} ${titleText}`;
            }
        } else if (p.name) {
            titleText = `${pCode} (${p.name})`;
        }
        
        const pAlias = p.alias ? `<p style="margin: 0.5rem 0 0 0; font-size: 0.95rem; color: #cbd5e1;">別名: ${highlight(p.alias, tokens)}</p>` : '';
        
        let boxHtml = `
            <div class="product-box">
                <div class="product-header">
                    <h2 class="product-title">
                        ${isUnclassified ? '📦 未分類の書類' : `📦 製品: ${highlight(titleText, tokens)}`}
                        ${group.seibans && group.seibans.length ? group.seibans.map(s => `<span class="badge badge-seiban">製番: ${escapeHtml(s)}</span>`).join('') : ''}
                    </h2>
                    ${isUnclassified ? `<span class="badge badge-unclassified">未分類</span>` : ''}
                    ${(p.name === '未登録部品' || p.name === '未登録製品(依頼書)') ? `<button class="btn btn-secondary" style="margin-left: 1rem; padding: 2px 8px; font-size: 0.85rem;" onclick="registerProductName('${escapeHtml(pCode).replace(/'/g, "\\\\'")}')">製品名を登録する</button>` : ''}
                    ${pAlias}
                </div>
        `;

        // Render BOMs
        if (group.boms && group.boms.length > 0) {
            boxHtml += `
                <div class="section">
                    <div class="section-header" onclick="this.parentElement.classList.toggle('open')">
                        <span>📋 BOM (${group.boms.length}件)</span>
                    </div>
                    <div class="section-content">
                        <div class="section-inner">
            `;
            group.boms.forEach(b => {
                let compsHtml = '';
                if (b.components && b.components.length > 0) {
                    compsHtml = `<div class="table-wrap"><table><tr><th>役割</th><th>部品番号</th><th>仕様メモ</th></tr>`;
                    if (Array.isArray(b.components)) {
                        b.components.forEach(c => {
                            let isRedText = c.role === '【特記・赤字】';
                            let style = isRedText ? 'color: #ff6b6b; font-weight: bold;' : '';
                            if (!b.layout_ok) {
                                style += ' opacity: 0.7;';
                            }
                            compsHtml += `<tr style="${style}">
                                <td>${highlight(c.role, tokens)}</td>
                                <td>${createTag(c.part_no, 'part')}</td>
                                <td>${highlight(c.note, tokens)}</td>
                            </tr>`;
                        });
                    } else {
                        compsHtml += `<tr><td colspan="3"><pre style="white-space:pre-wrap; font-size:11px; color:#666;">${escapeHtml(String(b.components))}</pre></td></tr>`;
                    }
                    compsHtml += `</table></div>`;
                }

                boxHtml += `
                    <div class="item-card">
                        <h4>BOM: ${escapeHtml(b.file.replace(/\\/g, '/').split('/').pop())} 
                            ${b.is_exception ? (b.layout_ok ? '<span class="badge" style="background:#20c997; color:white;">例外レイアウト・確認済</span>' : '<span class="badge badge-warn">例外レイアウト・要確認</span>') : ''}
                        </h4>
                        ${b.ref_requests ? `<div>関連依頼: ${b.ref_requests.map(r => createTag('#'+r)).join(' ')}</div>` : ''}
                        ${compsHtml}
                        <div class="action-bar">
                            <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(b.previews))}, ${escapeHtml(JSON.stringify(b.file))})'>プレビュー</button>
                            ${b.sp_url ? `<a href="${b.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (b.file ? `<a href="/${b.file.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excelを開く</a>` : '')}
                            ${!b.layout_ok ? `<button class="btn btn-secondary" style="border:1px solid var(--danger);color:var(--danger)" onclick='openAIConfirm(${escapeHtml(JSON.stringify(b))})'>AI解析を確定</button>` : ''}
                        </div>
                    </div>
                `;
            });
            boxHtml += `</div></div></div>`;
        }

        // Render Requests
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
                            ${r.sp_url ? `<a href="${r.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (r.file ? `<a href="/${r.file.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel/画像を開く</a>` : '')}
                            ${r.is_handwritten ? `<button class="btn btn-secondary" onclick="updateHinmei('${escapeHtml(r.request_no)}', '${escapeHtml(r.hinmei)}')">品名を編集</button>` : ''}
                        </div>
                    </div>
                `;
            });
            boxHtml += `</div></div></div>`;
        }

        // Render Inspections
        if (group.inspections && group.inspections.length > 0) {
             boxHtml += `
                <div class="section">
                    <div class="section-header" onclick="this.parentElement.classList.toggle('open')">
                        <span>✅ 検査証 (${group.inspections.length}件)</span>
                    </div>
                    <div class="section-content">
                        <div class="section-inner">
            `;
            group.inspections.forEach(i => {
                boxHtml += `
                    <div class="item-card">
                        <h4>${escapeHtml(i.file_path.replace(/\\/g, '/').split('/').pop())}</h4>
                        <div class="action-bar">
                            <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(i.previews))}, ${escapeHtml(JSON.stringify(i.file_path))})'>プレビュー</button>
                            ${i.sp_url ? `<a href="${i.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (i.file_path ? `<a href="/${i.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">開く</a>` : '')}
                        </div>
                    </div>
                `;
            });
            boxHtml += `</div></div></div>`;
        }
        
        // Render Photos
        if (group.photos && group.photos.length > 0) {
             boxHtml += `
                <div class="section">
                    <div class="section-header" onclick="this.parentElement.classList.toggle('open')">
                        <span>📸 写真 (${group.photos.length}件)</span>
                    </div>
                    <div class="section-content">
                        <div class="section-inner">
            `;
            group.photos.forEach(p => {
                boxHtml += `
                    <div class="item-card">
                        <h4>${escapeHtml(p.file_path.replace(/\\/g, '/').split('/').pop())}</h4>
                        <img src="/${p.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" style="max-width:100%;border-radius:4px;margin-bottom:0.5rem">
                        <div class="action-bar">
                            ${p.file_path ? `<a href="/${p.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">開く</a>` : ''}
                        </div>
                    </div>
                `;
            });
            boxHtml += `</div></div></div>`;
        }
        
        // Render Drawings
        if (group.drawings && group.drawings.length > 0) {
            boxHtml += `
               <div class="section">
                   <div class="section-header" onclick="this.parentElement.classList.toggle('open')">
                       <span>📐 図面 (${group.drawings.length}件)</span>
                   </div>
                   <div class="section-content">
                       <div class="section-inner">
           `;
           group.drawings.forEach(d => {
               boxHtml += `
                   <div class="item-card">
                       <h4>${escapeHtml(d.file_path.replace(/\\/g, '/').split('/').pop())}</h4>
                       <div class="action-bar">
                           ${d.previews && d.previews.length > 0 && d.previews[0] !== 'previews/dummy_0.png' ? `<button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(d.previews))}, ${escapeHtml(JSON.stringify(d.file_path))})'>プレビュー</button>` : ''}
                           ${d.sp_url ? `<a href="${d.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (SharePoint)</a>` : ''}
                          ${d.file_path ? `<a href="/${d.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">ローカルで開く</a>` : ''}
                       </div>
                   </div>
               `;
           });
           boxHtml += `</div></div></div>`;
       }

        boxHtml += `</div>`; // Close product box
        html += boxHtml;
    });

    resultsContainer.innerHTML = html;
}

function renderRequestSearch(groups, tokens) {
    let html = '';
    let reqBoxes = [];

    // Map to group by Request
    groups.forEach(g => {
        if (g.requests && g.requests.length > 0) {
            g.requests.forEach(req => {
                reqBoxes.push({
                    request: req,
                    product: g.product,
                    boms: g.boms || [],
                    inspections: g.inspections || [],
                    photos: g.photos || [],
                    drawings: g.drawings || []
                });
            });
        }
    });

    // Sort reqBoxes by request_no descending
    reqBoxes.sort((a, b) => {
        const numA = parseInt(a.request.request_no) || 0;
        const numB = parseInt(b.request.request_no) || 0;
        return numB - numA;
    });

    const totalFound = reqBoxes.length;
    reqBoxes = reqBoxes.slice(0, 100);

    statsContainer.textContent = `加工依頼書: ${totalFound}件見つかりました${totalFound > 100 ? ' (最新100件を表示)' : ''}`;

    if (reqBoxes.length === 0) {
        resultsContainer.innerHTML = '<div class="empty-state">該当する加工依頼書がありません</div>';
        return;
    }

    reqBoxes.forEach(box => {
        const r = box.request;
        const isModified = r.file && (r.file.includes('〇') || r.file.includes('×') || r.file.includes('修正'));
        let boxHtml = `
            <div class="product-group">
                <div class="group-header">
                    <h2>📄 依頼No: ${highlight(r.request_no, tokens)} ${r.seiban ? `(製番: ${highlight(r.seiban, tokens)})` : ''}</h2>
                    <p style="margin: 0.5rem 0 0 0; font-size: 0.95rem; color: #cbd5e1;">品名: ${highlight(r.hinmei, tokens)} | サイズ: ${escapeHtml(r.size)}</p>
                </div>
                <div class="group-content">
                    <div class="item-card ${isModified ? 'highlight-modified' : ''}" style="border: 2px solid var(--primary); margin-bottom: 1rem;">
                        <h4>加工依頼書: ${escapeHtml(r.file.replace(/\\/g, '/').split('/').pop())}
                            ${r.is_handwritten ? '<span class="badge badge-warn" style="margin-left: 8px;">⚠️手書き(要確認)</span>' : ''}
                            ${isModified ? '<span class="badge badge-warn" style="margin-left: 8px; background: #e74c3c;">⚠️修正/関連あり</span>' : ''}
                        </h4>
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
                            ${r.sp_url ? `<a href="${r.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (r.file ? `<a href="/${r.file.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel/画像を開く</a>` : '')}
                            ${r.is_handwritten ? `<button class="btn btn-secondary" onclick="updateHinmei('${escapeHtml(r.request_no)}', '${escapeHtml(r.hinmei)}')">品名を編集</button>` : ''}
                        </div>
                    </div>
        `;

        // Render related BOMs
        if (box.boms.length > 0) {
            boxHtml += `
                <div class="section">
                    <div class="section-header" onclick="this.parentElement.classList.toggle('open')">
                        <span>📋 関連BOM (${box.boms.length}件)</span>
                    </div>
                    <div class="section-content"><div class="section-inner">
            `;
            box.boms.forEach(b => {
                let compsHtml = '';
                if (b.components && b.components.length > 0) {
                    compsHtml = `<div class="table-wrap"><table><tr><th>役割</th><th>部品番号</th><th>仕様メモ</th></tr>`;
                    if (b.layout_ok) {
                        b.components.forEach(c => {
                            let isRedText = c.role === '【特記・赤字】';
                            let style = isRedText ? 'color: #ff6b6b; font-weight: bold;' : '';
                            compsHtml += `<tr style="${style}">
                                <td>${highlight(c.role, tokens)}</td>
                                <td>${createTag(c.part_no, 'part')}</td>
                                <td>${highlight(c.note, tokens)}</td>
                            </tr>`;
                        });
                    } else {
                        compsHtml += `<tr><td colspan="3"><pre style="white-space:pre-wrap">${escapeHtml(b.components)}</pre></td></tr>`;
                    }
                    compsHtml += `</table></div>`;
                }

                boxHtml += `
                    <div class="item-card">
                        <h4>BOM: ${escapeHtml(b.file.replace(/\\/g, '/').split('/').pop())} 
                            ${b.layout_ok ? '' : '<span class="badge badge-warn">例外レイアウト・要確認</span>'}
                        </h4>
                        ${compsHtml}
                        <div class="action-bar">
                            <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(b.previews))}, ${escapeHtml(JSON.stringify(b.file))})'>プレビュー</button>
                            ${b.sp_url ? `<a href="${b.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (b.file ? `<a href="/${b.file.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excelを開く</a>` : '')}
                        </div>
                    </div>
                `;
            });
            boxHtml += `</div></div></div>`;
        }

        // Render related Inspections
        if (box.inspections.length > 0) {
            boxHtml += `
                <div class="section">
                    <div class="section-header" onclick="this.parentElement.classList.toggle('open')">
                        <span>🔍 関連検査証 (${box.inspections.length}件)</span>
                    </div>
                    <div class="section-content"><div class="section-inner" style="display:flex; flex-wrap:wrap; gap:1rem">
            `;
            box.inspections.forEach(i => {
                boxHtml += `
                    <div class="item-card" style="flex:1; min-width:250px">
                        <h4>${escapeHtml(i.file_path.replace(/\\/g, '/').split('/').pop())}</h4>
                        <div class="action-bar">
                            <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(i.previews))}, ${escapeHtml(JSON.stringify(i.file_path))})'>プレビュー</button>
                            ${i.sp_url ? `<a href="${i.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (i.file_path ? `<a href="/${i.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">開く</a>` : '')}
                        </div>
                    </div>
                `;
            });
            boxHtml += `</div></div></div>`;
        }

        // Render related Photos
        if (box.photos.length > 0) {
            boxHtml += `
                <div class="section">
                    <div class="section-header" onclick="this.parentElement.classList.toggle('open')">
                        <span>📷 関連写真・その他 (${box.photos.length}件)</span>
                    </div>
                    <div class="section-content"><div class="section-inner" style="display:flex; flex-wrap:wrap; gap:1rem">
            `;
            box.photos.forEach(p => {
                boxHtml += `
                    <div class="item-card" style="flex:1; min-width:250px">
                        <h4>${escapeHtml(p.file_path.replace(/\\/g, '/').split('/').pop())}</h4>
                        <img src="/${p.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" style="max-width:100%; border-radius:4px; margin-bottom:0.5rem">
                        <div class="action-bar">
                            ${p.file_path ? `<a href="/${p.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">開く</a>` : ''}
                        </div>
                    </div>
                `;
            });
            boxHtml += `</div></div></div>`;
        }

        // Render related Drawings
        if (box.drawings.length > 0) {
            boxHtml += `
                <div class="section">
                    <div class="section-header" onclick="this.parentElement.classList.toggle('open')">
                        <span>📐 関連図面 (${box.drawings.length}件)</span>
                    </div>
                    <div class="section-content"><div class="section-inner" style="display:flex; flex-wrap:wrap; gap:1rem">
            `;
            box.drawings.forEach(d => {
                boxHtml += `
                    <div class="item-card" style="flex:1; min-width:250px">
                        <h4>${escapeHtml(d.file_path.replace(/\\/g, '/').split('/').pop())}</h4>
                        <div class="action-bar">
                            ${d.previews && d.previews.length > 0 && d.previews[0] !== 'previews/dummy_0.png' ? `<button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(d.previews))}, ${escapeHtml(JSON.stringify(d.file_path))})'>プレビュー</button>` : ''}
                            ${d.sp_url ? `<a href="${d.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (SharePoint)</a>` : ''}
                          ${d.file_path ? `<a href="/${d.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">ローカルで開く</a>` : ''}
                        </div>
                    </div>
                `;
            });
            boxHtml += `</div></div></div>`;
        }

        boxHtml += `</div></div>`;
        html += boxHtml;
    });

    resultsContainer.innerHTML = html;
}

function renderGlobalSearch(groups, tokens, state) {
    let html = '';
    
    // Flatten all data
    let allBoms = [];
    let allReqs = [];
    let allInsps = [];
    let allPhotos = [];
    let allDrawings = [];
    
    groups.forEach(g => {
        if(g.boms) allBoms = allBoms.concat(g.boms.map(b => ({...b, _product: g.product})));
        if(g.requests) allReqs = allReqs.concat(g.requests.map(r => ({...r, _product: g.product})));
        if(g.inspections) allInsps = allInsps.concat(g.inspections.map(i => ({...i, _product: g.product})));
        if(g.photos) allPhotos = allPhotos.concat(g.photos.map(p => ({...p, _product: g.product})));
        if(g.drawings) allDrawings = allDrawings.concat(g.drawings.map(d => ({...d, _product: g.product})));
    });

    // Apply strict filtering based on inputs
    if (state.req) {
        const sReq = state.req.toLowerCase();
        allBoms = allBoms.filter(b => b.ref_requests && b.ref_requests.some(r => r.toLowerCase().includes(sReq)));
        allReqs = allReqs.filter(r => r.request_no && String(r.request_no).toLowerCase().includes(sReq));
        allInsps = [];
        allPhotos = [];
    }

    if (state.part) {
        const sPart = state.part.toLowerCase();
        allBoms = allBoms.filter(b => b.components && b.components.some(c => c.part_no && c.part_no.toLowerCase().includes(sPart)));
        allReqs = [];
        allInsps = [];
        allPhotos = [];
    }

    // Sort requests by request_no descending
    allReqs.sort((a, b) => {
        const numA = parseInt(a.request_no) || 0;
        const numB = parseInt(b.request_no) || 0;
        return numB - numA;
    });

    const showBom = document.getElementById('filterBom').checked;
    const showReq = document.getElementById('filterReq').checked;
    const showInsp = document.getElementById('filterInsp').checked;
    const showPhoto = document.getElementById('filterPhoto').checked;
    const showDrawing = document.getElementById('filterDrawing').checked;

    let items = [];
    if (showBom) items = items.concat(allBoms.map(x => ({...x, _type: 'bom'})));
    if (showReq) items = items.concat(allReqs.map(x => ({...x, _type: 'req'})));
    if (showInsp) items = items.concat(allInsps.map(x => ({...x, _type: 'insp'})));
    if (showPhoto) items = items.concat(allPhotos.map(x => ({...x, _type: 'photo'})));
    if (showDrawing) items = items.concat(allDrawings.map(x => ({...x, _type: 'drawing'})));

    let totalHits = 0;
    if (showBom) totalHits += allBoms.length;
    if (showReq) totalHits += allReqs.length;
    if (showInsp) totalHits += allInsps.length;
    if (showPhoto) totalHits += allPhotos.length;
    if (showDrawing) totalHits += allDrawings.length;

    statsContainer.textContent = `全体で ${totalHits} 件ヒットしました`;

    // Render BOMs Flat
    if (showBom && allBoms.length > 0) {
        html += `<div class="flat-section"><h3>📋 BOM一覧 (${allBoms.length}件)</h3>`;
        allBoms.forEach(b => {
            let compsHtml = '';
            if (b.components && b.components.length > 0) {
                compsHtml = `<div class="table-wrap" style="margin-bottom:1rem"><table><tr><th>役割</th><th>部品番号</th><th>仕様メモ</th></tr>`;
                b.components.forEach(c => {
                    let isRedText = c.role === '【特記・赤字】';
                    let style = isRedText ? 'color: #ff6b6b; font-weight: bold;' : '';
                    compsHtml += `<tr style="${style}">
                        <td>${highlight(c.role, tokens)}</td>
                        <td>${createTag(c.part_no, 'part')}</td>
                        <td>${highlight(c.note, tokens)}</td>
                    </tr>`;
                });
                compsHtml += `</table></div>`;
            }
            html += `
                <div class="item-card">
                    <h4>${escapeHtml(b.file.replace(/\\/g, '/').split('/').pop())}</h4>
                    <p style="margin:0 0 0.5rem 0; font-size:0.85rem; color:var(--text-muted)">
                        製番: ${highlight(b.seiban, tokens)} | 品名: ${highlight(b._product && b._product.name, tokens)}
                    </p>
                    ${compsHtml}
                    <div class="action-bar">
                        <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(b.previews))}, ${escapeHtml(JSON.stringify(b.file))})'>プレビュー</button>
                        ${b.sp_url ? `<a href="${b.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (b.file ? `<a href="/${b.file.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excelを開く</a>` : '')}
                    </div>
                </div>
            `;
        });
        html += `</div>`;
    }

    // Render Requests Flat
    if (showReq && allReqs.length > 0) {
        html += `<div class="flat-section"><h3>📄 加工依頼書一覧 (${allReqs.length}件)</h3>`;
        allReqs.forEach(r => {
            const isModified = r.file && (r.file.includes('〇') || r.file.includes('×') || r.file.includes('修正'));
            html += `
                <div class="item-card ${isModified ? 'highlight-modified' : ''}">
                    <h4>${escapeHtml(r.file.replace(/\\/g, '/').split('/').pop())}
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
                        ${r.sp_url ? `<a href="${r.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (r.file ? `<a href="/${r.file.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel/画像を開く</a>` : '')}
                        ${r.is_handwritten ? `<button class="btn btn-secondary" onclick="updateHinmei('${escapeHtml(r.request_no)}', '${escapeHtml(r.hinmei)}')">品名を編集</button>` : ''}
                    </div>
                </div>
            `;
        });
        html += `</div>`;
    }

    // Render Inspections Flat
    if (showInsp && allInsps.length > 0) {
        html += `<div class="flat-section"><h3>🔍 検査証一覧 (${allInsps.length}件)</h3><div style="display:flex; flex-wrap:wrap; gap:1rem">`;
        allInsps.forEach(i => {
            html += `
                <div class="item-card" style="flex:1; min-width:300px">
                    <h4>${escapeHtml(i.file_path.replace(/\\/g, '/').split('/').pop())}</h4>
                    <div class="action-bar">
                        <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(i.previews))}, ${escapeHtml(JSON.stringify(i.file_path))})'>プレビュー</button>
                        ${i.sp_url ? `<a href="${i.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (i.file_path ? `<a href="/${i.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">開く</a>` : '')}
                    </div>
                </div>
            `;
        });
        html += `</div></div>`;
    }

    // Render Photos Flat
    if (showPhoto && allPhotos.length > 0) {
        html += `<div class="flat-section"><h3>📷 写真・その他一覧 (${allPhotos.length}件)</h3><div style="display:flex; flex-wrap:wrap; gap:1rem">`;
        allPhotos.forEach(p => {
            const pName = p._product && p._product.name ? ` (${p._product.name})` : '';
            const pCode = p._product ? p._product.product_code : '未分類';
            html += `
                <div class="item-card" style="flex:1; min-width:300px">
                    <h4>${escapeHtml(p.file_path.replace(/\\/g, '/').split('/').pop())}</h4>
                    <p style="font-size:0.85rem; color:var(--text-muted); margin: 0 0 0.5rem 0;">関連製品: ${escapeHtml(pCode)}${escapeHtml(pName)}</p>
                    <img src="/${p.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}?t=${Date.now()}" style="max-width:100%; border-radius:4px; margin-bottom:0.5rem">
                    <div class="action-bar">
                        ${p.file_path ? `<a href="/${p.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">開く</a>` : ''}
                    </div>
                </div>
            `;
        });
        html += `</div></div>`;
    }
    
    // Render Drawings Flat
    if (showDrawing && allDrawings.length > 0) {
        html += `<div class="flat-section"><h3>📐 図面一覧 (${allDrawings.length}件)</h3><div style="display:flex; flex-wrap:wrap; gap:1rem">`;
        allDrawings.forEach(d => {
            const pName = d._product && d._product.name ? ` (${d._product.name})` : '';
            const pCode = d._product ? d._product.product_code : '未分類';
            html += `
                <div class="item-card" style="flex:1; min-width:250px">
                    <h4>${escapeHtml(d.file_path.replace(/\\/g, '/').split('/').pop())}</h4>
                    <p style="font-size:0.85rem; color:var(--text-muted); margin: 0 0 0.5rem 0;">関連製品: ${escapeHtml(pCode)}${escapeHtml(pName)}</p>
                    <div class="action-bar">
                        ${d.previews && d.previews.length > 0 && d.previews[0] !== 'previews/dummy_0.png' ? `<button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(d.previews))}, ${escapeHtml(JSON.stringify(d.file_path))})'>プレビュー</button>` : ''}
                        ${d.file_path ? `<a href="/${d.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">ダウンロード / 開く</a>` : ''}
                    </div>
                </div>
            `;
        });
        html += `</div></div>`;
    }

    if (html === '') {
        html = '<div class="empty-state">チェックされた項目に該当するデータがありません</div>';
    }
    
    resultsContainer.innerHTML = html;
}

// Modal handling
