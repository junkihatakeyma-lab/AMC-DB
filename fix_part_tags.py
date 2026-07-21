with open('static/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Update createTag function
old_createTag = """function createTag(text) {
    if (!text) return '';
    return `<span class="tag" onclick="triggerTagSearch('${text.replace(/'/g, "\\\\'")}')">${escapeHtml(text)}</span>`;
}"""

new_createTag = """function createTag(text, type) {
    if (!text) return '';
    return `<span class="tag" onclick="triggerTagSearch('${text.replace(/'/g, "\\\\'")}', '${type || ''}')">${escapeHtml(text)}</span>`;
}"""

content = content.replace(old_createTag, new_createTag)

# Update triggerTagSearch function
old_trigger = """window.triggerTagSearch = function(keyword) {
    document.getElementById('searchInput').value = '';
    document.getElementById('searchSeiban').value = '';
    document.getElementById('searchReq').value = '';
    document.getElementById('searchProduct').value = '';
    document.getElementById('searchPart').value = '';
    document.getElementById('searchDrawing').value = '';
    
    if (keyword.startsWith('#')) {
        document.getElementById('searchReq').value = keyword.substring(1);
    } else {
        document.getElementById('searchInput').value = keyword;
    }
    
    performSearch();
};"""

new_trigger = """window.triggerTagSearch = function(keyword, type) {
    document.getElementById('searchInput').value = '';
    document.getElementById('searchSeiban').value = '';
    document.getElementById('searchReq').value = '';
    document.getElementById('searchProduct').value = '';
    document.getElementById('searchPart').value = '';
    document.getElementById('searchDrawing').value = '';
    
    if (type === 'part') {
        document.getElementById('searchPart').value = keyword;
    } else if (keyword.startsWith('#')) {
        document.getElementById('searchReq').value = keyword.substring(1);
    } else {
        document.getElementById('searchInput').value = keyword;
    }
    
    performSearch();
};"""

content = content.replace(old_trigger, new_trigger)

# Replace all createTag(c.part_no) with createTag(c.part_no, 'part')
content = content.replace("createTag(c.part_no)", "createTag(c.part_no, 'part')")

with open('static/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated createTag successfully!")
