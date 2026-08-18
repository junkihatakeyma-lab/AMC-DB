import re
import codecs

with codecs.open('static/app.js', 'r', 'utf-8') as f:
    content = f.read()

# The block to replace:
#                             <div class="table-wrap">
#                                 <table>
#                                     <tr><th>発行日</th><td>${escapeHtml(r.issue_date)}</td></tr>
#                                     <tr><th>数量</th><td>${escapeHtml(r.qty)}</td></tr>
#                                     <tr><th>生地色</th><td>${highlight(r.kiji, tokens)}</td></tr>
#                                     <tr><th>用途</th><td>${highlight(r.yoto, tokens)}</td></tr>
#                                     <tr><th>納期</th><td>${escapeHtml(r.noki || r.noki_raw)}</td></tr>
#                                     <tr><th>出荷先</th><td>${highlight(r.dest, tokens)}</td></tr>
#                                     <tr><th>規格</th><td><pre style="margin:0;font-family:inherit;white-space:pre-wrap">${highlight(r.spec, tokens)}</pre></td></tr>
#                                     <tr><th>備考</th><td><pre style="margin:0;font-family:inherit;white-space:pre-wrap">${highlight(r.biko, tokens)}</pre></td></tr>
#                                 </table>
#                             </div>

new_block = """                            <div class="table-wrap">
                                ${(() => {
                                    const matchingBoms = group.boms.filter(b => b.ref_requests && b.ref_requests.includes(r.request_no));
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
                            </div>"""

# Ensure we only replace inside the handReqs loop.
# It is located after `handReqs.forEach(r => {`
start_idx = content.find('handReqs.forEach(r => {')
if start_idx != -1:
    end_idx = content.find('// Render Inspections', start_idx)
    sub_content = content[start_idx:end_idx]
    
    # regex to match the table-wrap block
    pattern = r'<div class="table-wrap">\s*<table>\s*<tr><th>発行日.*?</table>\s*</div>'
    sub_content = re.sub(pattern, new_block, sub_content, flags=re.DOTALL)
    
    content = content[:start_idx] + sub_content + content[end_idx:]

    with codecs.open('static/app.js', 'w', 'utf-8') as f:
        f.write(content)
    print("Replaced successfully!")
else:
    print("Could not find handReqs.forEach block")

