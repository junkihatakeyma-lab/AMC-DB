def patch(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the target string by looking for the <th> row
    old1 = '<th>役割</th><th>部品番号</th><th>仕様メモ</th></tr>'
    new1 = '<th>役割</th><th>部品番号</th><th>仕様メモ</th><th>マスタ情報</th></tr>'

    if old1 in content:
        content = content.replace(old1, new1)
        print("Replaced headers")
    
    # Find the target string for the loop
    old2 = '<td>${highlight(c.note, tokens)}</td>'
    new2 = """<td>${highlight(c.note, tokens)}</td>
                                <td>${(c.master && c.master.master_id) ? `<div style="font-size: 0.85em; color: #2c3e50; background: #e8f4f8; padding: 4px; border-radius: 4px;">` + [`品名: ${c.master.hinmei||''}`, `寸法: ${c.master.k_sunpo||''}`, `材質: ${c.master.zaishitsu||''}`].filter(s=>!s.endsWith(': ')).map(s=>escapeHtml(s)).join('<br>') + `</div>` : ''}</td>"""

    if old2 in content:
        content = content.replace(old2, new2)
        print("Replaced cells")
        
    # Also fix colspan="3"
    content = content.replace('colspan="3"', 'colspan="4"')
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filename}")

patch('build_clean_app2.py')
patch('static/app_raw.js')
