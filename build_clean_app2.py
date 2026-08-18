import re
import json

with open('static/app_raw.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove everything from performSearch to the end of the file
# and we will re-inject performSearch and the render functions.
start = text.find('async function performSearch()')
if start == -1:
    print('Could not find performSearch')
    exit(1)

head = text[:start]

new_code = r"""
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

// --- FIREBASE AUTH LOGIC ---
let isDataLoaded = false;

document.addEventListener('DOMContentLoaded', () => {
    // Wait a brief moment to ensure Firebase script is loaded
    // (Firebase compat scripts are defer, so DOMContentLoaded is usually fine, 
    // but sometimes firebase is undefined if network is weird, though defer guarantees order)
    if (typeof firebase === 'undefined') {
        console.error("Firebase SDK not loaded");
        document.getElementById('loginError').textContent = "システムエラー: Firebase SDKが読み込めません。再読み込みしてください。";
        document.getElementById('loginError').style.display = 'block';
        return;
    }
    
    firebase.auth().onAuthStateChanged((user) => {
        if (user) {
            // User is signed in.
            document.getElementById('loginOverlay').style.display = 'none';
            document.getElementById('appHeader').style.display = 'block';
            document.getElementById('appMain').style.display = 'block';
            document.getElementById('userEmail').textContent = user.email;
            
            if (!isDataLoaded) {
                loadData();
                isDataLoaded = true;
            }
        } else {
            // No user is signed in.
            document.getElementById('loginOverlay').style.display = 'flex';
            document.getElementById('appHeader').style.display = 'none';
            document.getElementById('appMain').style.display = 'none';
            
            // Clear data for security/privacy on logout
            GLOBAL_DATA = [];
            lastGroups = [];
            isDataLoaded = false;
            document.getElementById('results').innerHTML = '';
            document.getElementById('stats').textContent = '';
            if (typeof clearAllSearch === 'function') clearAllSearch();
        }
    });
});

window.login = async function() {
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;
    const errEl = document.getElementById('loginError');
    errEl.style.display = 'none';
    
    if (!email || !password) {
        errEl.textContent = "メールアドレスとパスワードを入力してください。";
        errEl.style.display = 'block';
        return;
    }
    
    try {
        await firebase.auth().signInWithEmailAndPassword(email, password);
        // onAuthStateChanged will handle the UI switch
    } catch (error) {
        console.error(error);
        errEl.textContent = "ログインに失敗しました: " + error.message;
        errEl.style.display = 'block';
    }
};

window.signup = async function() {
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;
    const errEl = document.getElementById('loginError');
    errEl.style.display = 'none';
    
    if (!email || !password) {
        errEl.textContent = "メールアドレスとパスワードを入力してください。";
        errEl.style.display = 'block';
        return;
    }
    
    if (password.length < 6) {
        errEl.textContent = "パスワードは6文字以上にしてください。";
        errEl.style.display = 'block';
        return;
    }
    
    try {
        await firebase.auth().createUserWithEmailAndPassword(email, password);
        // onAuthStateChanged will handle the UI switch
    } catch (error) {
        console.error(error);
        errEl.textContent = "登録に失敗しました: " + error.message;
        errEl.style.display = 'block';
    }
};

window.logout = async function() {
    try {
        await firebase.auth().signOut();
    } catch (error) {
        console.error("Logout Error", error);
    }
};


function createTag(text, type) {
    if (!text) return '';
    return `<span class="tag" onclick="triggerTagSearch('${String(text).replace(/'/g, "\\'")}', '${type || ''}')">${escapeHtml(text)}</span>`;
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

    const search_seiban = normalize(seiban);
    const search_req = normalize(req);
    const search_product = normalize(product);
    const search_part = part.split(/\s+/).map(normalize).filter(v=>v);
    const search_company = normalize(company);
    const search_q = q.split(/\s+/).map(normalize).filter(v=>v);

    const resultsContainer = document.getElementById('results');
    const statsContainer = document.getElementById('stats');
    resultsContainer.innerHTML = '<div style="text-align:center; padding: 2rem; color: #666;">検索中...</div>';
    statsContainer.textContent = '';
    
    await new Promise(r => setTimeout(r, 50));

    let filteredGroups = [];

    for (let g of GLOBAL_DATA) {
        if (!g.boms.length && !g.requests.length && !g.inspections.length && !g.photos.length && !g.drawings.length) continue;

        let match_seiban = true;
        let match_req = true;
        let match_product = true;
        let match_company = true;
        let match_part = true;
        let match_q = true;

        if (search_seiban && !normalize(g._search_seiban || '').includes(search_seiban)) match_seiban = false;
        if (search_req && !normalize(g._search_req || '').includes(search_req)) match_req = false;
        if (search_product && !normalize(g._search_product || '').includes(search_product)) match_product = false;
        if (search_company && !normalize(g._search_company || '').includes(search_company)) match_company = false;
        
        if (search_part.length > 0) {
            for (let token of search_part) {
                if (!normalize(g._search_part || '').includes(token)) {
                    match_part = false; break;
                }
            }
        }
        if (search_q.length > 0) {
            for (let token of search_q) {
                if (!normalize(g._search_all || '').includes(token)) {
                    match_q = false; break;
                }
            }
        }

        if (match_seiban && match_req && match_product && match_company && match_part && match_q) {
            let g_out = JSON.parse(JSON.stringify(g));
            
            // Filter children only if specific fields are typed
            if (search_seiban || search_req || search_part.length > 0 || search_company) {
                if (search_seiban) {
                    if (g_out.boms) g_out.boms = g_out.boms.filter(b => normalize(b.seiban || '').includes(search_seiban));
                    if (g_out.requests) g_out.requests = g_out.requests.filter(r => normalize(r.seiban || '').includes(search_seiban));
                }
                if (search_req) {
                    if (g_out.boms) g_out.boms = g_out.boms.filter(b => b.ref_requests && b.ref_requests.some(r_ref => normalize(r_ref).includes(search_req)));
                    if (g_out.requests) g_out.requests = g_out.requests.filter(r => normalize(r.request_no || '').includes(search_req));
                }
                if (search_part.length > 0) {
                    if (g_out.boms) {
                        g_out.boms = g_out.boms.filter(b => {
                            if (!b.components) return false;
                            return search_part.every(token => {
                                return b.components.some(c => normalize(c.part_no || '').includes(token));
                            });
                        });
                    }
                }
            }
            
            let totalBoms = g_out.boms ? g_out.boms.length : 0;
            let totalReqs = g_out.requests ? g_out.requests.length : 0;
            let totalInsps = g_out.inspections ? g_out.inspections.length : 0;
            let totalPhotos = g_out.photos ? g_out.photos.length : 0;
            let totalDrawings = g_out.drawings ? g_out.drawings.length : 0;
            
            if (totalBoms + totalReqs + totalInsps + totalPhotos + totalDrawings > 0) {
                filteredGroups.push(g_out);
            }
        }
    }

    lastGroups = filteredGroups;
    const state = { q, seiban, req_no: req, product, part_no: part, company: company };
    renderResults(filteredGroups, state);
}

function renderResults(groups, state) {
    let tokens = Object.values(state).filter(x => x).join(' ').split(/\s+/).filter(x => x);
    
    const resultsContainer = document.getElementById('results');
    const statsContainer = document.getElementById('stats');

    if (!groups || groups.length === 0) {
        statsContainer.textContent = '該当するデータがありません';
        resultsContainer.innerHTML = '';
        return;
    }

    if (currentTab === 'product') {
        renderProductSearch(groups, tokens, resultsContainer, statsContainer);
    } else if (currentTab === 'request') {
        renderRequestSearch(groups, tokens, resultsContainer, statsContainer);
    } else {
        renderGlobalSearch(groups, tokens, state, resultsContainer, statsContainer);
    }
}

function renderProductSearch(groups, tokens, resultsContainer, statsContainer) {
    let html = '';
    
    let displayGroups = groups;
    if (groups.length > 50) {
        displayGroups = groups.slice(0, 50);
        statsContainer.textContent = `${groups.length} 製品箱が見つかりました (検索結果が多すぎるため上位50件のみ表示)`;
    } else {
        statsContainer.textContent = `${groups.length} 製品箱が見つかりました`;
    }

    displayGroups.forEach(group => {
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
                        <h4>BOM: ${escapeHtml((b.file || '').replace(/\\/g, '/').split('/').pop())} 
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

        // Split requests into handwritten and non-handwritten
        const reqs = group.requests || [];
        const handReqs = reqs.filter(r => r.is_handwritten);
        const otherReqs = reqs.filter(r => !r.is_handwritten);
        
        // Render Handwritten Requests
        if (handReqs.length > 0) {
            handReqs.sort((a, b) => (parseInt(b.request_no) || 0) - (parseInt(a.request_no) || 0));
            boxHtml += `
                <div class="section">
                    <div class="section-header" onclick="this.parentElement.classList.toggle('open')">
                        <span>✍️ 加工依頼書_BOM一体 (${handReqs.length}件)</span>
                    </div>
                    <div class="section-content">
                        <div class="section-inner">
            `;
            handReqs.forEach(r => {
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
                            ${r.sp_url ? `<a href="${r.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (r.file ? `<a href="/${r.file.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel/画像を開く</a>` : '')}
                            <button class="btn btn-secondary" onclick="updateHinmei('${escapeHtml(r.request_no)}', '${escapeHtml(r.hinmei)}')">品名を編集</button>
                        </div>
                    </div>
                `;
            });
            boxHtml += `</div></div></div>`;
        }
        
        // Render Normal Requests
        if (otherReqs.length > 0) {
            otherReqs.sort((a, b) => (parseInt(b.request_no) || 0) - (parseInt(a.request_no) || 0));
            boxHtml += `
                <div class="section">
                    <div class="section-header" onclick="this.parentElement.classList.toggle('open')">
                        <span>📝 加工依頼書 (${otherReqs.length}件)</span>
                    </div>
                    <div class="section-content">
                        <div class="section-inner">
            `;
            otherReqs.forEach(r => {
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
                            ${r.sp_url ? `<a href="${r.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">🌐 ブラウザで開く (Excel for Web)</a>` : (r.file ? `<a href="/${r.file.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel/画像を開く</a>` : '')}
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
"""

with open('static/app_raw.js', 'r', encoding='utf-8') as f:
    text = f.read()

# For the other render functions, we can just extract them from app_raw.js
# and paste them to keep it simple, but wait...
# They are fine in app_raw.js! We just need to extract from renderRequestSearch down to window.openPreview
req_start = text.find('function renderRequestSearch')
preview_start = text.find('window.openPreview = function')
tail_renders = text[req_start:preview_start]

tail = text[preview_start:]

final_js = head + new_code + '\n' + tail_renders + '\n' + tail

with open('static/app.js', 'w', encoding='utf-8-sig') as f:
    f.write(final_js)

print("Generated app.js successfully.")
