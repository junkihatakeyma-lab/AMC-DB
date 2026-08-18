const searchInput = document.getElementById('searchInput');
const resultsContainer = document.getElementById('results');
const statsContainer = document.getElementById('stats');
const modal = document.getElementById('modal');
const modalBody = document.getElementById('modalBody');
const modalTitle = document.getElementById('modalTitle');
const modalOpenOriginal = document.getElementById('modalOpenOriginal');
const modalClose = document.getElementById('modalClose');
const inputs = ['searchInput', 'searchSeiban', 'searchReq', 'searchProduct', 'searchPart', 'searchCompany'];

window.openAIConfirm = async function(bom) {
    alert('message');
}

window.registerProductName = async function(pCode) {
    alert('message');
};

window.updateHinmei = async function(reqNo, oldHinmei) {
    alert('message');
};

let currentLinkPartNo = null;

window.openLinkModal = function(partNo) {
    currentLinkPartNo = partNo;
    document.getElementById('linkModalPartNo').innerText = 'error';
    document.getElementById('linkModalMasterId').value = '';
    document.getElementById('linkModalError').style.display = 'none';
    document.getElementById('linkModal').style.display = 'flex';
};

window.closeLinkModal = function() {
    document.getElementById('linkModal').style.display = 'none';
    currentLinkPartNo = null;
};

window.saveLinkModal = async function() {
    const masterId = document.getElementById('linkModalMasterId').value.trim();
    if (!masterId) {
        document.getElementById('linkModalError').innerText = 'error';
        document.getElementById('linkModalError').style.display = 'block';
        return;
    }
    
    try {
        const db = firebase.firestore();
        await db.collection("manual_part_links").doc(currentLinkPartNo).set({
            db_part_no: currentLinkPartNo,
            master_id: masterId,
            updated_at: firebase.firestore.FieldValue.serverTimestamp()
        });
        
        alert('message');
        closeLinkModal();
    } catch (e) {
        console.error("Firestore error: ", e);
        document.getElementById('linkModalError').innerText = 'error';
        document.getElementById('linkModalError').style.display = 'block';
    }
};

let currentTab = 'product';
let lastGroups = [];

window.switchTab = function(tabName) {
    currentTab = tabName;
    document.getElementById('tabProduct').classList.toggle('active', tabName === 'product');
    document.getElementById('tabRequest').classList.toggle('active', tabName === 'request');
    document.getElementById('tabGlobal').classList.toggle('active', tabName === 'global');
    document.getElementById('globalFilters').style.display = tabName === 'global' ? 'flex' : 'none';
    
    const state = {
        q: document.getElementById('searchInput').value.trim(),
        seiban: document.getElementById('searchSeiban').value.trim(),
        req_no: document.getElementById('searchReq').value.trim(),
        product: document.getElementById('searchProduct').value.trim(),
        part_no: Array.from(document.querySelectorAll('.searchPartInput')).map(i => i.value.trim()).filter(v => v !== '').join(' '),
        company: document.getElementById('searchCompany').value.trim()
    };
    // Re-render based on current tab
    renderResults(lastGroups, state);
};
let searchTimeout;
inputs.forEach(id => {
    const el = document.getElementById(id);
    if(el) {
        el.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch();
            }, 300);
        });
    }
});

// Helper to escape HTML and highlight search tokens
function escapeHtml(str) {
    if (str == null) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function highlight(str, tokens) {
    let esc = escapeHtml(str);
    if (!esc || tokens.length === 0) return esc;
    
    tokens.forEach(t => {
        if (t.length < 2) return; // Don't highlight single characters
        try {
            const regex = new RegExp(t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
            esc = esc.replace(regex, match => `<mark>${match}</mark>`);
        } catch (e) {}
    });
    return esc;
}


window.addPartInput = function(val = '') {
    const list = document.getElementById('partInputsList');
    const currentInputs = list.querySelectorAll('.part-input-row');
    if (currentInputs.length >= 5) {
        alert('message');
        return;
    }

    const row = document.createElement('div');
    row.className = 'part-input-row';
    row.style = 'display: flex; gap: 4px; flex: 1;';
    
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'searchPartInput';
    input.placeholder = '霑ｽ蜉�縺ｮ驛ｨ蜩∫分蜿ｷ';
    input.value = val;
    input.style = 'width: 100%;';
    input.addEventListener('input', () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(performSearch, 300);
    });
    
    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.className = 'btn btn-secondary';
    removeBtn.innerText = 'X';
    removeBtn.style = 'padding: 0 8px; border-radius: 4px; background: #e74c3c; color: white; border: none; cursor: pointer; height: 100%;';
    removeBtn.onclick = function() {
        row.remove();
        document.getElementById('addPartBtn').disabled = false;
    };
    
    row.appendChild(input);
    row.appendChild(removeBtn);
    list.appendChild(row);
    
    if (currentInputs.length + 1 >= 5) {
        document.getElementById('addPartBtn').disabled = true;
    }
};

// Perform search via API
window.clearAllSearch = function() {
    ['searchInput', 'searchSeiban', 'searchReq', 'searchProduct', 'searchCompany'].forEach(id => {
        document.getElementById(id).value = '';
    });
    const list = document.getElementById('partInputsList');
    if (list) {
        list.innerHTML = `
            <div class="part-input-row" style="display: flex; gap: 4px;">
                <input type="text" class="searchPartInput" placeholder="萓・ IF000-304" style="flex: 1;">
            </div>
        `;
        document.querySelector('.searchPartInput').addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(performSearch, 300);
        });
        document.getElementById('addPartBtn').disabled = false;
    }
    performSearch();
};

let GLOBAL_DATA = [];

// Wait for Firebase to initialize
document.addEventListener("DOMContentLoaded", () => {
    // 認証機能を一時的に無効化し、直接データを読み込む
    /*
    firebase.auth().onAuthStateChanged(async (user) => {
        const overlay = document.getElementById('loginOverlay');
        const appContainer = document.getElementById('appContainer');
        const errorDiv = document.getElementById('loginError');

        if (user) {
            // Check domain
            if (user.email && user.email.endsWith('@amc-inc.jp')) {
                overlay.style.display = 'none';
                appContainer.style.display = 'block';
                errorDiv.style.display = 'none';
                await loadData();
            } else {
                // Invalid domain
                await firebase.auth().signOut();
                errorDiv.innerText = 'error';
                errorDiv.style.display = 'block';
                overlay.style.display = 'flex';
                appContainer.style.display = 'none';
            }
        } else {
            // Not logged in
            overlay.style.display = 'flex';
            appContainer.style.display = 'none';
        }
    });
    */
    loadData();
});

window.signInWithGoogle = async function() {
    const provider = new firebase.auth.GoogleAuthProvider();
    // Allow selecting account if they have multiple
    provider.setCustomParameters({ prompt: 'select_account' });
    try {
        await firebase.auth().signInWithPopup(provider);
    } catch (error) {
        console.error("Login failed", error);
        const errorDiv = document.getElementById('loginError');
        errorDiv.innerText = 'error';
        errorDiv.style.display = 'block';
    }
}

window.signOut = async function() {
    await firebase.auth().signOut();
}

// Load data.json from Firebase Cloud Storage
async function loadData() {
    try {
        const res = await fetch('/data.json');
        GLOBAL_DATA = await res.json();
        performSearch(''); // Render initial UI
    } catch (e) {
        console.error(e);
    }
}

async function performSearch() {
    const seiban = document.getElementById('searchSeiban').value.trim();
    const req = document.getElementById('searchReq').value.trim();
    const product = document.getElementById('searchProduct').value.trim();
    const partInputs = Array.from(document.querySelectorAll('.searchPartInput')).map(i => i.value.trim()).filter(v => v !== '');
    const part = partInputs.join(' ');
    const company = document.getElementById('searchCompany').value.trim();
    const q = document.getElementById('searchInput').value.trim();

    if (!q && !seiban && !req && !product && !part && !company) {
        document.getElementById('results').innerHTML = '<div class="empty-state">no results</div>';
        return;
    }

    // Helper for normalization
    const normalize = (text) => {
        if (!text) return "";
        let t = String(text).toLowerCase();
        t = t.replace(/[A-Za-z0-9]/g, function(s) {
            return String.fromCharCode(s.charCodeAt(0) - 0xFEE0);
        });
        t = t.replace(/[＃]/g, '#').replace(/[ー−―‐]/g, '-');
        return t;
    };

    const search_q = q ? normalize(q).split(/\s+/) : [];
    const search_seiban = normalize(seiban);
    const search_req = normalize(req);
    const search_product = normalize(product);
    const search_part = part ? normalize(part).split(/\s+/) : [];
    const search_company = normalize(company);

    let results = [];

    for (let g of GLOBAL_DATA) {
        if (!g.boms.length && !g.requests.length && !g.inspections.length && !g.photos.length && !g.drawings.length) continue;

        let match_seiban = true;
        let match_req = true;
        let match_product = true;
        let match_part = true;
        let match_company = true;
        let match_general = true;

        if (search_seiban && !g._search_seiban.includes(search_seiban)) match_seiban = false;
        if (search_req && !g._search_req.includes(search_req)) match_req = false;
        if (search_product && !g._search_product.includes(search_product)) match_product = false;
        if (search_part.length > 0) {
            for (let token of search_part) {
                if (!g._search_part.includes(token)) {
                    match_part = false; break;
                }
            }
        }
        if (search_company && !(g._search_company || '').includes(search_company)) match_company = false;
        if (search_q.length > 0) {
            for (let token of search_q) {
                if (!g._search_text.includes(token)) {
                    match_general = false; break;
                }
            }
        }

        if (match_seiban && match_req && match_product && match_part && match_company && match_general) {
            // Deep clone to avoid mutating GLOBAL_DATA when filtering inner arrays
            let g_out = JSON.parse(JSON.stringify(g));

            if (search_req && g_out.requests) {
                g_out.requests = g_out.requests.filter(r => normalize(r.request_no).includes(search_req));
            }

            if (!g_out.product && g_out.requests) {
                g_out.requests.sort((a, b) => {
                    const numA = parseInt(String(a.request_no).replace(/\D/g, '')) || 0;
                    const numB = parseInt(String(b.request_no).replace(/\D/g, '')) || 0;
                    return numB - numA;
                });
                g_out.requests = g_out.requests.slice(0, 100);
            }

            if (search_seiban && g_out.boms) {
                g_out.boms = g_out.boms.filter(b => normalize(b.seiban).includes(search_seiban));
            }

            if (search_part.length > 0 && g_out.boms) {
                g_out.boms = g_out.boms.filter(b => {
                    if (!b.components) return false;
                    for (let token of search_part) {
                        let tokenFound = false;
                        if (typeof b.components === 'string') {
                            if (normalize(b.components).includes(token)) tokenFound = true;
                        } else {
                            for (let c of b.components) {
                                if (normalize(c.part_no).includes(token)) {
                                    tokenFound = true; break;
                                }
                            }
                        }
                        if (!tokenFound) return false;
                    }
                    return true;
                });
            }

            results.append ? results.append(g_out) : results.push(g_out);
            if (results.length >= 200) break;
        }
    }

    lastGroups = results;
    const state = { q, seiban, req_no: req, product, part_no: part, company };
    renderResults(results, state);
    
    if (results.length >= 200) {
        resultsContainer.insertAdjacentHTML('beforeend', '<div style="text-align:center; padding:1.5rem; margin-top:1rem; border-top:1px solid var(--border); color:var(--text-muted);">邃ｹ・・邨先棡縺悟､壹☆縺弱ｋ縺溘ａ縲∽ｸ贋ｽ・00莉ｶ縺ｮ縺ｿ繧定｡ｨ遉ｺ縺励※縺・∪縺吶ゅ＆繧峨↓譚｡莉ｶ繧堤ｵ槭ｊ霎ｼ繧薙〒縺上□縺輔＞縲・/div>');
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
                    <input type="text" class="searchPartInput" placeholder="萓・ IF000-304" style="width: 100%;">
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
        statsContainer.textContent = '隧ｲ蠖薙☆繧九ョ繝ｼ繧ｿ縺後≠繧翫∪縺帙ｓ';
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
    statsContainer.textContent = `${groups.length} 陬ｽ蜩∫ｮｱ縺瑚ｦ九▽縺九ｊ縺ｾ縺励◆`;

    groups.forEach(group => {
        const p = group.product || {};
        const isUnclassified = !p.product_code;
        const pCode = p.product_code || 'Unknown';
        let titleText = pCode;
        if (p.name && p.name !== 'UnregisteredPart' && p.name !== 'UnregisteredProduct') {
            titleText = p.name;
            if (!titleText.includes(pCode)) {
                titleText = `${pCode} ${titleText}`;
            }
        } else if (p.name) {
            titleText = `${pCode} (${p.name})`;
        }
        
        const pAlias = p.alias ? `<p style="margin: 0.5rem 0 0 0; font-size: 0.95rem; color: #cbd5e1;">蛻･蜷・ ${highlight(p.alias, tokens)}</p>` : '';
        
        let boxHtml = `
            <div class="product-box">
                <div class="product-header">
                    <h2 class="product-title">
                        ${isUnclassified ? 'Unclassified' : `�逃 陬ｽ蜩・ ${highlight(titleText, tokens)}`}
                        ${group.seibans && group.seibans.length ? group.seibans.map(s => `<span class="badge badge-seiban">陬ｽ逡ｪ: ${escapeHtml(s)}</span>`).join('') : ''}
                    </h2>
                    ${isUnclassified ? `<span class="badge badge-unclassified">譛ｪ蛻・｡・/span>` : ''}
                    ${(p.name === 'Unregistered') ? `<button class="btn btn-secondary" style="margin-left: 1rem; padding: 2px 8px; font-size: 0.85rem;" onclick="registerProductName('${escapeHtml(pCode).replace(/'/g, "\\\\'")}')">陬ｽ蜩∝錐繧堤匳骭ｲ縺吶ｋ</button>` : ''}
                    ${pAlias}
                </div>
        `;

        // Render BOMs
        if (group.boms && group.boms.length > 0) {
            boxHtml += `
                <div class="section">
                    <div class="section-header" onclick="this.parentElement.classList.toggle('open')">
                        <span>�搭 BOM (${group.boms.length}莉ｶ)</span>
                    </div>
                    <div class="section-content">
                        <div class="section-inner">
            `;
            group.boms.forEach(b => {
                let compsHtml = '';
                if (b.components && b.components.length > 0) {
                    compsHtml = `<div class="table-wrap"><table><tr><th>蠖ｹ蜑ｲ</th><th>驛ｨ蜩∫分蜿ｷ</th><th>蜩∝錐(繝槭せ繧ｿ)</th><th>莉墓ｧ・繝槭せ繧ｿ)</th><th>莉墓ｧ倥Γ繝｢</th></tr>`;
                    if (Array.isArray(b.components)) {
                        b.components.forEach(c => {
                            let isRedText = c.role === 'RedText';
                            let style = isRedText ? 'color: #ff6b6b; font-weight: bold;' : '';
                            if (!b.layout_ok) {
                                style += ' opacity: 0.7;';
                            }
                            compsHtml += `<tr style="${style}">
                                <td>${highlight(c.role, tokens)}</td>
                                <td>
                                    ${createTag(c.part_no, 'part')}
                                    ${c.master ? '<span title="繝槭せ繧ｿ邏蝉ｻ倥￠貂・ style="color:#20c997; margin-left:4px; font-size:14px;">�迫</span>' : '<span title="譛ｪ邏蝉ｻ倥￠" style="color:#e74c3c; margin-left:4px; font-size:14px;">笶・/span>'}
                                    <button class="btn btn-secondary" style="padding: 1px 4px; font-size: 11px; margin-left: 4px;" onclick="openLinkModal('${escapeHtml(c.part_no).replace(/'/g, "\\\\'")}')">�統邏蝉ｻ・/button>
                                </td>
                                <td>${c.master ? highlight(c.master.hinmei, tokens) : ''}</td>
                                <td>${c.master ? highlight(c.master.k_sunpo, tokens) : ''}</td>
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
                            ${b.is_exception ? (b.layout_ok ? '<span class="badge" style="background:#20c997; color:white;">萓句､悶Ξ繧､繧｢繧ｦ繝医・遒ｺ隱肴ｸ・/span>' : '<span class="badge badge-warn">萓句､悶Ξ繧､繧｢繧ｦ繝医・隕∫｢ｺ隱・/span>') : ''}
                        </h4>
                        ${b.ref_requests ? `<div>髢｢騾｣萓晞�ｼ: ${b.ref_requests.map(r => createTag('#'+r)).join(' ')}</div>` : ''}
                        ${compsHtml}
                        <div class="action-bar">
                            <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(b.previews))}, ${escapeHtml(JSON.stringify(b.file))})'>繝励Ξ繝薙Η繝ｼ</button>
                            ${b.sp_url ? `<a href="${b.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">�倹 繝悶Λ繧ｦ繧ｶ縺ｧ髢九￥ (Excel for Web)</a>` : (b.file ? `<a href="/${b.file.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel繧帝幕縺・/a>` : '')}
                            ${!b.layout_ok ? `<button class="btn btn-secondary" style="border:1px solid var(--danger);color:var(--danger)" onclick='openAIConfirm(${escapeHtml(JSON.stringify(b))})'>AI隗｣譫舌ｒ遒ｺ螳・/button>` : ''}
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
                        <span>�統 蜉�蟾･萓晞�ｼ譖ｸ (${group.requests.length}莉ｶ)</span>
                    </div>
                    <div class="section-content">
                        <div class="section-inner">
            `;
            group.requests.forEach(r => {
                const isModified = false;
                boxHtml += `
                    <div class="item-card ${isModified ? 'highlight-modified' : ''}">
                        <h4>萓晞�ｼ譖ｸ #${r.request_no} ${highlight(r.hinmei, tokens)} 
                            ${r.is_handwritten ? '<span class="badge badge-warn" style="margin-left: 8px;">笞�・乗焔譖ｸ縺・隕∫｢ｺ隱・</span>' : ''}
                            ${isModified ? '<span class="badge badge-warn" style="margin-left: 8px; background: #e74c3c;">笞�・丈ｿｮ豁｣/髢｢騾｣縺ゅｊ</span>' : ''}
                        </h4>
                        <div class="table-wrap">
                            <table>
                                <tr><th>逋ｺ陦梧律</th><td>${escapeHtml(r.issue_date)}</td></tr>
                                <tr><th>謨ｰ驥・/th><td>${escapeHtml(r.qty)}</td></tr>
                                <tr><th>逕溷慍濶ｲ</th><td>${highlight(r.kiji, tokens)}</td></tr>
                                <tr><th>逕ｨ騾・/th><td>${highlight(r.yoto, tokens)}</td></tr>
                                <tr><th>邏肴悄</th><td>${escapeHtml(r.noki || r.noki_raw)}</td></tr>
                                <tr><th>蜃ｺ闕ｷ蜈・/th><td>${highlight(r.dest, tokens)}</td></tr>
                                <tr><th>隕乗�ｼ</th><td><pre style="margin:0;font-family:inherit;white-space:pre-wrap">${highlight(r.spec, tokens)}</pre></td></tr>
                                <tr><th>蛯呵・/th><td><pre style="margin:0;font-family:inherit;white-space:pre-wrap">${highlight(r.biko, tokens)}</pre></td></tr>
                            </table>
                        </div>
                        <div class="action-bar">
                            <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(r.previews))}, ${escapeHtml(JSON.stringify(r.file))})'>繝励Ξ繝薙Η繝ｼ</button>
                            ${r.sp_url ? `<a href="${r.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">�倹 繝悶Λ繧ｦ繧ｶ縺ｧ髢九￥ (Excel for Web)</a>` : (r.file ? `<a href="/${r.file.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel/逕ｻ蜒上ｒ髢九￥</a>` : '')}
                            ${r.is_handwritten ? `<button class="btn btn-secondary" onclick="updateHinmei('${escapeHtml(r.request_no)}', '${escapeHtml(r.hinmei)}')">蜩∝錐繧堤ｷｨ髮・/button>` : ''}
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
                        <span>笨・讀懈渊險ｼ (${group.inspections.length}莉ｶ)</span>
                    </div>
                    <div class="section-content">
                        <div class="section-inner">
            `;
            group.inspections.forEach(i => {
                boxHtml += `
                    <div class="item-card">
                        <h4>${escapeHtml(i.file_path.replace(/\\/g, '/').split('/').pop())}</h4>
                        <div class="action-bar">
                            <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(i.previews))}, ${escapeHtml(JSON.stringify(i.file_path))})'>繝励Ξ繝薙Η繝ｼ</button>
                            ${i.sp_url ? `<a href="${i.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">�倹 繝悶Λ繧ｦ繧ｶ縺ｧ髢九￥ (Excel for Web)</a>` : (i.file_path ? `<a href="/${i.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">髢九￥</a>` : '')}
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
                        <span>�萄 蜀咏悄 (${group.photos.length}莉ｶ)</span>
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
                            ${p.file_path ? `<a href="/${p.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">髢九￥</a>` : ''}
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
                       <span>�盗 蝗ｳ髱｢ (${group.drawings.length}莉ｶ)</span>
                   </div>
                   <div class="section-content">
                       <div class="section-inner">
           `;
           group.drawings.forEach(d => {
               boxHtml += `
                   <div class="item-card">
                       <h4>${escapeHtml(d.file_path.replace(/\\/g, '/').split('/').pop())}</h4>
                       <div class="action-bar">
                           ${d.previews && d.previews.length > 0 && d.previews[0] !== 'previews/dummy_0.png' ? `<button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(d.previews))}, ${escapeHtml(JSON.stringify(d.file_path))})'>繝励Ξ繝薙Η繝ｼ</button>` : ''}
                           ${d.sp_url ? `<a href="${d.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">�倹 繝悶Λ繧ｦ繧ｶ縺ｧ髢九￥ (SharePoint)</a>` : ''}
                          ${d.file_path ? `<a href="/${d.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">繝ｭ繝ｼ繧ｫ繝ｫ縺ｧ髢九￥</a>` : ''}
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

    statsContainer.textContent = `蜉�蟾･萓晞�ｼ譖ｸ: ${totalFound}莉ｶ隕九▽縺九ｊ縺ｾ縺励◆${totalFound > 100 ? ' (譛譁ｰ100莉ｶ繧定｡ｨ遉ｺ)' : ''}`;

    if (reqBoxes.length === 0) {
        resultsContainer.innerHTML = '<div class="empty-state">no results</div>';
        return;
    }

    reqBoxes.forEach(box => {
        const r = box.request;
        const isModified = false;
        let boxHtml = `
            <div class="product-group">
                <div class="group-header">
                    <h2>�塘 萓晞�ｼNo: ${highlight(r.request_no, tokens)} ${r.seiban ? `(陬ｽ逡ｪ: ${highlight(r.seiban, tokens)})` : ''}</h2>
                    <p style="margin: 0.5rem 0 0 0; font-size: 0.95rem; color: #cbd5e1;">蜩∝錐: ${highlight(r.hinmei, tokens)} | 繧ｵ繧､繧ｺ: ${escapeHtml(r.size)}</p>
                </div>
                <div class="group-content">
                    <div class="item-card ${isModified ? 'highlight-modified' : ''}" style="border: 2px solid var(--primary); margin-bottom: 1rem;">
                        <h4>蜉�蟾･萓晞�ｼ譖ｸ: ${escapeHtml(r.file.replace(/\\/g, '/').split('/').pop())}
                            ${r.is_handwritten ? '<span class="badge badge-warn" style="margin-left: 8px;">笞�・乗焔譖ｸ縺・隕∫｢ｺ隱・</span>' : ''}
                            ${isModified ? '<span class="badge badge-warn" style="margin-left: 8px; background: #e74c3c;">笞�・丈ｿｮ豁｣/髢｢騾｣縺ゅｊ</span>' : ''}
                        </h4>
                        <div class="table-wrap" style="margin-bottom:0.5rem">
                            <table>
                                <tr><th>蜩∝錐</th><td>${highlight(r.hinmei, tokens)}</td><th>謨ｰ驥・/th><td>${highlight(r.qty, tokens)}</td></tr>
                                <tr><th>逕溷慍</th><td>${highlight(r.kiji, tokens)}</td><th>逕ｨ騾・/th><td>${highlight(r.yoto, tokens)}</td></tr>
                                <tr><th>莉墓ｧ・/th><td colspan="3">${highlight(r.spec, tokens)}</td></tr>
                                <tr><th>蛯呵・/th><td colspan="3">${highlight(r.biko, tokens)}</td></tr>
                            </table>
                        </div>
                        <div class="action-bar">
                            <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(r.previews))}, ${escapeHtml(JSON.stringify(r.file))})'>繝励Ξ繝薙Η繝ｼ</button>
                            ${r.sp_url ? `<a href="${r.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">�倹 繝悶Λ繧ｦ繧ｶ縺ｧ髢九￥ (Excel for Web)</a>` : (r.file ? `<a href="/${r.file.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel/逕ｻ蜒上ｒ髢九￥</a>` : '')}
                            ${r.is_handwritten ? `<button class="btn btn-secondary" onclick="updateHinmei('${escapeHtml(r.request_no)}', '${escapeHtml(r.hinmei)}')">蜩∝錐繧堤ｷｨ髮・/button>` : ''}
                        </div>
                    </div>
        `;

        // Render related BOMs
        if (box.boms.length > 0) {
            boxHtml += `
                <div class="section">
                    <div class="section-header" onclick="this.parentElement.classList.toggle('open')">
                        <span>�搭 髢｢騾｣BOM (${box.boms.length}莉ｶ)</span>
                    </div>
                    <div class="section-content"><div class="section-inner">
            `;
            box.boms.forEach(b => {
                let compsHtml = '';
                if (b.components && b.components.length > 0) {
                    compsHtml = `<div class="table-wrap"><table><tr><th>蠖ｹ蜑ｲ</th><th>驛ｨ蜩∫分蜿ｷ</th><th>蜩∝錐(繝槭せ繧ｿ)</th><th>莉墓ｧ・繝槭せ繧ｿ)</th><th>莉墓ｧ倥Γ繝｢</th></tr>`;
                    if (b.layout_ok) {
                        b.components.forEach(c => {
                            let isRedText = c.role === 'RedText';
                            let style = isRedText ? 'color: #ff6b6b; font-weight: bold;' : '';
                            compsHtml += `<tr style="${style}">
                                <td>${highlight(c.role, tokens)}</td>
                                <td>
                                    ${createTag(c.part_no, 'part')}
                                    ${c.master ? '<span title="繝槭せ繧ｿ邏蝉ｻ倥￠貂・ style="color:#20c997; margin-left:4px; font-size:14px;">�迫</span>' : '<span title="譛ｪ邏蝉ｻ倥￠" style="color:#e74c3c; margin-left:4px; font-size:14px;">笶・/span>'}
                                    <button class="btn btn-secondary" style="padding: 1px 4px; font-size: 11px; margin-left: 4px;" onclick="openLinkModal('${escapeHtml(c.part_no).replace(/'/g, "\\\\'")}')">�統邏蝉ｻ・/button>
                                </td>
                                <td>${c.master ? highlight(c.master.hinmei, tokens) : ''}</td>
                                <td>${c.master ? highlight(c.master.k_sunpo, tokens) : ''}</td>
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
                            ${b.layout_ok ? '' : '<span class="badge badge-warn">萓句､悶Ξ繧､繧｢繧ｦ繝医・隕∫｢ｺ隱・/span>'}
                        </h4>
                        ${compsHtml}
                        <div class="action-bar">
                            <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(b.previews))}, ${escapeHtml(JSON.stringify(b.file))})'>繝励Ξ繝薙Η繝ｼ</button>
                            ${b.sp_url ? `<a href="${b.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">�倹 繝悶Λ繧ｦ繧ｶ縺ｧ髢九￥ (Excel for Web)</a>` : (b.file ? `<a href="/${b.file.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel繧帝幕縺・/a>` : '')}
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
                        <span>�剥 髢｢騾｣讀懈渊險ｼ (${box.inspections.length}莉ｶ)</span>
                    </div>
                    <div class="section-content"><div class="section-inner" style="display:flex; flex-wrap:wrap; gap:1rem">
            `;
            box.inspections.forEach(i => {
                boxHtml += `
                    <div class="item-card" style="flex:1; min-width:250px">
                        <h4>${escapeHtml(i.file_path.replace(/\\/g, '/').split('/').pop())}</h4>
                        <div class="action-bar">
                            <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(i.previews))}, ${escapeHtml(JSON.stringify(i.file_path))})'>繝励Ξ繝薙Η繝ｼ</button>
                            ${i.sp_url ? `<a href="${i.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">�倹 繝悶Λ繧ｦ繧ｶ縺ｧ髢九￥ (Excel for Web)</a>` : (i.file_path ? `<a href="/${i.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">髢九￥</a>` : '')}
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
                        <span>�胴 髢｢騾｣蜀咏悄繝ｻ縺昴・莉・(${box.photos.length}莉ｶ)</span>
                    </div>
                    <div class="section-content"><div class="section-inner" style="display:flex; flex-wrap:wrap; gap:1rem">
            `;
            box.photos.forEach(p => {
                boxHtml += `
                    <div class="item-card" style="flex:1; min-width:250px">
                        <h4>${escapeHtml(p.file_path.replace(/\\/g, '/').split('/').pop())}</h4>
                        <img src="/${p.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" style="max-width:100%; border-radius:4px; margin-bottom:0.5rem">
                        <div class="action-bar">
                            ${p.file_path ? `<a href="/${p.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">髢九￥</a>` : ''}
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
                        <span>�盗 髢｢騾｣蝗ｳ髱｢ (${box.drawings.length}莉ｶ)</span>
                    </div>
                    <div class="section-content"><div class="section-inner" style="display:flex; flex-wrap:wrap; gap:1rem">
            `;
            box.drawings.forEach(d => {
                boxHtml += `
                    <div class="item-card" style="flex:1; min-width:250px">
                        <h4>${escapeHtml(d.file_path.replace(/\\/g, '/').split('/').pop())}</h4>
                        <div class="action-bar">
                            ${d.previews && d.previews.length > 0 && d.previews[0] !== 'previews/dummy_0.png' ? `<button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(d.previews))}, ${escapeHtml(JSON.stringify(d.file_path))})'>繝励Ξ繝薙Η繝ｼ</button>` : ''}
                            ${d.sp_url ? `<a href="${d.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">�倹 繝悶Λ繧ｦ繧ｶ縺ｧ髢九￥ (SharePoint)</a>` : ''}
                          ${d.file_path ? `<a href="/${d.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">繝ｭ繝ｼ繧ｫ繝ｫ縺ｧ髢九￥</a>` : ''}
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

    statsContainer.textContent = `Total ${totalHits} results`;

    // Render BOMs Flat
    if (showBom && allBoms.length > 0) {
        html += `<div class="flat-section"><h3>�搭 BOM荳隕ｧ (${allBoms.length}莉ｶ)</h3>`;
        allBoms.forEach(b => {
            let compsHtml = '';
            if (b.components && b.components.length > 0) {
                compsHtml = `<div class="table-wrap" style="margin-bottom:1rem"><table><tr><th>蠖ｹ蜑ｲ</th><th>驛ｨ蜩∫分蜿ｷ</th><th>莉墓ｧ倥Γ繝｢</th></tr>`;
                b.components.forEach(c => {
                    let isRedText = c.role === 'RedText';
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
                        陬ｽ逡ｪ: ${highlight(b.seiban, tokens)} | 蜩∝錐: ${highlight(b._product && b._product.name, tokens)}
                    </p>
                    ${compsHtml}
                    <div class="action-bar">
                        <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(b.previews))}, ${escapeHtml(JSON.stringify(b.file))})'>繝励Ξ繝薙Η繝ｼ</button>
                        ${b.sp_url ? `<a href="${b.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">�倹 繝悶Λ繧ｦ繧ｶ縺ｧ髢九￥ (Excel for Web)</a>` : (b.file ? `<a href="/${b.file.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel繧帝幕縺・/a>` : '')}
                    </div>
                </div>
            `;
        });
        html += `</div>`;
    }

    // Render Requests Flat
    if (showReq && allReqs.length > 0) {
        html += `<div class="flat-section"><h3>�塘 蜉�蟾･萓晞�ｼ譖ｸ荳隕ｧ (${allReqs.length}莉ｶ)</h3>`;
        allReqs.forEach(r => {
            const isModified = false;
            html += `
                <div class="item-card ${isModified ? 'highlight-modified' : ''}">
                    <h4>${escapeHtml(r.file.replace(/\\/g, '/').split('/').pop())}
                        ${r.is_handwritten ? '<span class="badge badge-warn" style="margin-left: 8px;">笞�・乗焔譖ｸ縺・隕∫｢ｺ隱・</span>' : ''}
                        ${isModified ? '<span class="badge badge-warn" style="margin-left: 8px; background: #e74c3c;">笞�・丈ｿｮ豁｣/髢｢騾｣縺ゅｊ</span>' : ''}
                    </h4>
                    <p style="margin:0 0 0.5rem 0; font-size:0.85rem; color:var(--text-muted)">
                        萓晞�ｼNo: ${highlight(r.request_no, tokens)} | 陬ｽ逡ｪ: ${highlight(r.seiban, tokens)}
                    </p>
                    <div class="table-wrap" style="margin-bottom:0.5rem">
                        <table>
                            <tr><th>蜩∝錐</th><td>${highlight(r.hinmei, tokens)}</td><th>謨ｰ驥・/th><td>${highlight(r.qty, tokens)}</td></tr>
                            <tr><th>逕溷慍</th><td>${highlight(r.kiji, tokens)}</td><th>逕ｨ騾・/th><td>${highlight(r.yoto, tokens)}</td></tr>
                            <tr><th>莉墓ｧ・/th><td colspan="3">${highlight(r.spec, tokens)}</td></tr>
                            <tr><th>蛯呵・/th><td colspan="3">${highlight(r.biko, tokens)}</td></tr>
                        </table>
                    </div>
                    <div class="action-bar">
                        <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(r.previews))}, ${escapeHtml(JSON.stringify(r.file))})'>繝励Ξ繝薙Η繝ｼ</button>
                        ${r.sp_url ? `<a href="${r.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">�倹 繝悶Λ繧ｦ繧ｶ縺ｧ髢九￥ (Excel for Web)</a>` : (r.file ? `<a href="/${r.file.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">Excel/逕ｻ蜒上ｒ髢九￥</a>` : '')}
                        ${r.is_handwritten ? `<button class="btn btn-secondary" onclick="updateHinmei('${escapeHtml(r.request_no)}', '${escapeHtml(r.hinmei)}')">蜩∝錐繧堤ｷｨ髮・/button>` : ''}
                    </div>
                </div>
            `;
        });
        html += `</div>`;
    }

    // Render Inspections Flat
    if (showInsp && allInsps.length > 0) {
        html += `<div class="flat-section"><h3>�剥 讀懈渊險ｼ荳隕ｧ (${allInsps.length}莉ｶ)</h3><div style="display:flex; flex-wrap:wrap; gap:1rem">`;
        allInsps.forEach(i => {
            html += `
                <div class="item-card" style="flex:1; min-width:300px">
                    <h4>${escapeHtml(i.file_path.replace(/\\/g, '/').split('/').pop())}</h4>
                    <div class="action-bar">
                        <button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(i.previews))}, ${escapeHtml(JSON.stringify(i.file_path))})'>繝励Ξ繝薙Η繝ｼ</button>
                        ${i.sp_url ? `<a href="${i.sp_url}" target="_blank" class="btn btn-primary" style="background:#0078d4; border-color:#0078d4;">�倹 繝悶Λ繧ｦ繧ｶ縺ｧ髢九￥ (Excel for Web)</a>` : (i.file_path ? `<a href="/${i.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">髢九￥</a>` : '')}
                    </div>
                </div>
            `;
        });
        html += `</div></div>`;
    }

    // Render Photos Flat
    if (showPhoto && allPhotos.length > 0) {
        html += `<div class="flat-section"><h3>�胴 蜀咏悄繝ｻ縺昴・莉紋ｸ隕ｧ (${allPhotos.length}莉ｶ)</h3><div style="display:flex; flex-wrap:wrap; gap:1rem">`;
        allPhotos.forEach(p => {
            const pName = p._product && p._product.name ? ` (${p._product.name})` : '';
            const pCode = p._product ? p._product.product_code : 'Unknown';
            html += `
                <div class="item-card" style="flex:1; min-width:300px">
                    <h4>${escapeHtml(p.file_path.replace(/\\/g, '/').split('/').pop())}</h4>
                    <p style="font-size:0.85rem; color:var(--text-muted); margin: 0 0 0.5rem 0;">髢｢騾｣陬ｽ蜩・ ${escapeHtml(pCode)}${escapeHtml(pName)}</p>
                    <img src="/${p.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}?t=${Date.now()}" style="max-width:100%; border-radius:4px; margin-bottom:0.5rem">
                    <div class="action-bar">
                        ${p.file_path ? `<a href="/${p.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">髢九￥</a>` : ''}
                    </div>
                </div>
            `;
        });
        html += `</div></div>`;
    }
    
    // Render Drawings Flat
    if (showDrawing && allDrawings.length > 0) {
        html += `<div class="flat-section"><h3>�盗 蝗ｳ髱｢荳隕ｧ (${allDrawings.length}莉ｶ)</h3><div style="display:flex; flex-wrap:wrap; gap:1rem">`;
        allDrawings.forEach(d => {
            const pName = d._product && d._product.name ? ` (${d._product.name})` : '';
            const pCode = d._product ? d._product.product_code : 'Unknown';
            html += `
                <div class="item-card" style="flex:1; min-width:250px">
                    <h4>${escapeHtml(d.file_path.replace(/\\/g, '/').split('/').pop())}</h4>
                    <p style="font-size:0.85rem; color:var(--text-muted); margin: 0 0 0.5rem 0;">髢｢騾｣陬ｽ蜩・ ${escapeHtml(pCode)}${escapeHtml(pName)}</p>
                    <div class="action-bar">
                        ${d.previews && d.previews.length > 0 && d.previews[0] !== 'previews/dummy_0.png' ? `<button class="btn btn-primary" onclick='openPreview(${escapeHtml(JSON.stringify(d.previews))}, ${escapeHtml(JSON.stringify(d.file_path))})'>繝励Ξ繝薙Η繝ｼ</button>` : ''}
                        ${d.file_path ? `<a href="/${d.file_path.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/')}" target="_blank" class="btn btn-secondary">繝繧ｦ繝ｳ繝ｭ繝ｼ繝・/ 髢九￥</a>` : ''}
                    </div>
                </div>
            `;
        });
        html += `</div></div>`;
    }

    if (html === '') {
        html = '<div class="empty-state">繝√ぉ繝・け縺輔ｌ縺滄�・岼縺ｫ隧ｲ蠖薙☆繧九ョ繝ｼ繧ｿ縺後≠繧翫∪縺帙ｓ</div>';
    }
    
    resultsContainer.innerHTML = html;
}

// Modal handling
window.openPreview = function(previews, originalFile) {
    modalTitle.textContent = originalFile.replace(/\\/g, '/').split('/').pop();
    const encodedOriginal = originalFile.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/');
    modalOpenOriginal.href = "/" + encodedOriginal;
    modalOpenOriginal.style.display = 'inline-flex';
    
    if (!previews || previews.length === 0 || previews[0] === 'previews/dummy_0.png') {
        modalBody.innerHTML = '<div style="text-align:center;padding:2rem">繝励Ξ繝薙Η繝ｼ逕ｻ蜒上′縺ゅｊ縺ｾ縺帙ｓ・・DF螟画鋤蠕・■縲√∪縺溘・譛ｪ逕滓・縺ｧ縺呻ｼ・/div>';
    } else {
        modalBody.innerHTML = previews.map(p => {
            const encodedPath = p.replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/');
            return `<img src="/${encodedPath}" class="preview-img">`;
        }).join('');
    }
    
    modal.classList.add('active');
};


modalClose.addEventListener('click', () => {
    modal.classList.remove('active');
});

modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.classList.remove('active');
    }
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') modal.classList.remove('active');
});

// Initial load
performSearch('');
