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

// Generate tag chips