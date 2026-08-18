import re

with open('static/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add modal logic at the bottom of the file
modal_logic = """
let currentLinkPartNo = null;

window.openLinkModal = function(partNo) {
    currentLinkPartNo = partNo;
    document.getElementById('linkModalPartNo').innerText = partNo;
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
        document.getElementById('linkModalError').innerText = 'マスタIDを入力してください。';
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
        
        alert('紐付けを保存しました。次回データ更新時に反映されます。');
        closeLinkModal();
    } catch (e) {
        console.error("Firestore error: ", e);
        document.getElementById('linkModalError').innerText = '保存に失敗しました。';
        document.getElementById('linkModalError').style.display = 'block';
    }
};
"""

if "window.openLinkModal" not in text:
    text += "\n" + modal_logic

# 2. Update components table rendering
old_table_headers = """<div class="table-wrap" style="margin-bottom:1rem"><table><tr><th>役割</th><th>部品番号</th><th>仕様メモ</th></tr>`;"""
new_table_headers = """<div class="table-wrap" style="margin-bottom:1rem"><table><tr><th style="width:10%;">役割</th><th style="width:25%;">部品番号</th><th style="width:20%;">品名 (マスタ)</th><th style="width:20%;">寸法 (マスタ)</th><th style="width:25%;">仕様メモ</th></tr>`;"""

old_table_row = """compsHtml += `<tr style="${style}">
                        <td>${highlight(c.role, tokens)}</td>
                        <td>${createTag(c.part_no, 'part')}</td>
                        <td>${highlight(c.note, tokens)}</td>
                    </tr>`;"""
new_table_row = """compsHtml += `<tr style="${style}">
                        <td>${highlight(c.role, tokens)}</td>
                        <td>${createTag(c.part_no, 'part')}
                            ${c.master ? '<span title="紐付け済み" style="color:#20c997; margin-left:4px; font-size:14px;">🔗</span>' : '<span title="未紐付け" style="color:#e74c3c; margin-left:4px; font-size:14px;">❌</span>'}
                            <button class="btn btn-secondary" style="padding: 1px 4px; font-size: 11px; margin-left: 4px;" onclick="openLinkModal('${escapeHtml(c.part_no).replace(/'/g, "\\\\'")}')">📝紐付</button>
                        </td>
                        <td>${c.master ? highlight(c.master.hinmei, tokens) : ''}</td>
                        <td>${c.master ? highlight(c.master.k_sunpo, tokens) : ''}</td>
                        <td>${highlight(c.note, tokens)}</td>
                    </tr>`;"""

text = text.replace(old_table_headers, new_table_headers)
text = text.replace(old_table_row, new_table_row)

with open('static/app.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Patch applied!")
