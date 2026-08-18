import re

with open('static/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

old_table_row = """<td>${createTag(c.part_no, 'part')}
                            ${c.master ? '<span title="紐付け済み" style="color:#20c997; margin-left:4px; font-size:14px;">🔗</span>' : '<span title="未紐付け" style="color:#e74c3c; margin-left:4px; font-size:14px;">❌</span>'}
                            <button class="btn btn-secondary" style="padding: 1px 4px; font-size: 11px; margin-left: 4px;" onclick="openLinkModal('${escapeHtml(c.part_no).replace(/'/g, "\\\\'")}')">📝紐付</button>
                        </td>"""

new_table_row = """<td>${createTag(c.part_no, 'part')}
                            ${(c.role === 'ラベル' || c.role === '【特記・赤字】') ? '' : 
                              (c.master ? '<span title="紐付け済み" style="color:#20c997; margin-left:4px; font-size:14px;">🔗</span>' : '<span title="未紐付け" style="color:#e74c3c; margin-left:4px; font-size:14px;">❌</span>')}
                            ${(c.role === 'ラベル' || c.role === '【特記・赤字】') ? '' : 
                              `<button class="btn btn-secondary" style="padding: 1px 4px; font-size: 11px; margin-left: 4px;" onclick="openLinkModal('${escapeHtml(c.part_no).replace(/'/g, "\\\\'")}')">📝紐付</button>`}
                        </td>"""

if old_table_row in text:
    text = text.replace(old_table_row, new_table_row)
    with open('static/app.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Successfully patched app.js to ignore labels and red text!")
else:
    print("Could not find the target string in app.js!")
