import re

with open('static/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update clearAllSearch
old_clear = """window.clearAllSearch = function() {
    ['searchInput', 'searchSeiban', 'searchReq', 'searchProduct', 'searchPart', 'searchDrawing'].forEach(id => {
        document.getElementById(id).value = '';
    });
    performSearch();
};"""
new_clear = """window.clearAllSearch = function() {
    ['searchInput', 'searchSeiban', 'searchReq', 'searchProduct', 'searchDrawing'].forEach(id => {
        document.getElementById(id).value = '';
    });
    const list = document.getElementById('partInputsList');
    if (list) {
        list.innerHTML = `
            <div class="part-input-row" style="display: flex; gap: 4px;">
                <input type="text" class="searchPartInput" placeholder="例: IF000-304" style="flex: 1;">
            </div>
        `;
        document.querySelector('.searchPartInput').addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(performSearch, 300);
        });
    }
    performSearch();
};"""
content = content.replace(old_clear, new_clear)

# 2. Add addPartInput
add_input_func = """
window.addPartInput = function(val = '') {
    const list = document.getElementById('partInputsList');
    const row = document.createElement('div');
    row.className = 'part-input-row';
    row.style = 'display: flex; gap: 4px;';
    
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'searchPartInput';
    input.placeholder = '追加の部品番号';
    input.value = val;
    input.style = 'flex: 1;';
    input.addEventListener('input', () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(performSearch, 300);
    });
    
    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.className = 'btn btn-secondary';
    removeBtn.innerText = '✖';
    removeBtn.style = 'padding: 0 8px; border-radius: 4px; background: #e74c3c; color: white; border: none; cursor: pointer;';
    removeBtn.onclick = function() {
        row.remove();
        // performSearch(); // Don't auto search on remove, let user click search
    };
    
    row.appendChild(input);
    row.appendChild(removeBtn);
    list.appendChild(row);
};
"""
content = content.replace("// Perform search via API", add_input_func + "\n// Perform search via API")

# 3. Update performSearch to gather all searchPartInput
old_perform1 = """const product = document.getElementById('searchProduct').value.trim();
    const part = document.getElementById('searchPart').value.trim();
    const drawing = document.getElementById('searchDrawing').value.trim();"""
new_perform1 = """const product = document.getElementById('searchProduct').value.trim();
    const partInputs = Array.from(document.querySelectorAll('.searchPartInput')).map(i => i.value.trim()).filter(v => v !== '');
    const part = partInputs.join(' ');
    const drawing = document.getElementById('searchDrawing').value.trim();"""
content = content.replace(old_perform1, new_perform1)

# 4. Update triggerTagSearch
old_trigger = """window.triggerTagSearch = function(keyword, type) {
    if (type === 'part') {
        const partInput = document.getElementById('searchPart');
        if (partInput.value) {
            if (!partInput.value.includes(keyword)) {
                partInput.value = partInput.value + ' ' + keyword;
            }
        } else {
            partInput.value = keyword;
        }
        document.getElementById('searchInput').value = '';
        document.getElementById('searchSeiban').value = '';
        document.getElementById('searchReq').value = '';
        document.getElementById('searchProduct').value = '';
        document.getElementById('searchDrawing').value = '';
        // Do NOT call performSearch() here so the UI doesn't refresh and close the BOM card.
    } else {
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
    }
};"""

new_trigger = """window.triggerTagSearch = function(keyword, type) {
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
        document.getElementById('searchDrawing').value = '';
    } else {
        document.getElementById('searchInput').value = '';
        document.getElementById('searchSeiban').value = '';
        document.getElementById('searchReq').value = '';
        document.getElementById('searchProduct').value = '';
        document.getElementById('searchDrawing').value = '';
        
        const list = document.getElementById('partInputsList');
        if (list) {
            list.innerHTML = `
                <div class="part-input-row" style="display: flex; gap: 4px;">
                    <input type="text" class="searchPartInput" placeholder="例: IF000-304" style="flex: 1;">
                </div>
            `;
            document.querySelector('.searchPartInput').addEventListener('input', () => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(performSearch, 300);
            });
        }
        
        if (keyword.startsWith('#')) {
            document.getElementById('searchReq').value = keyword.substring(1);
        } else {
            document.getElementById('searchInput').value = keyword;
        }
        performSearch();
    }
};"""
content = content.replace(old_trigger, new_trigger)

# 5. Fix the initialization to apply event listener to class instead of id
old_init = """['searchInput', 'searchSeiban', 'searchReq', 'searchProduct', 'searchPart', 'searchDrawing'].forEach(id => {
    document.getElementById(id).addEventListener('input', () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(performSearch, 300);
    });
});"""
new_init = """['searchInput', 'searchSeiban', 'searchReq', 'searchProduct', 'searchDrawing'].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
        el.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(performSearch, 300);
        });
    }
});
const firstPartInput = document.querySelector('.searchPartInput');
if (firstPartInput) {
    firstPartInput.addEventListener('input', () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(performSearch, 300);
    });
}"""
content = content.replace(old_init, new_init)

with open('static/app.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated app.js")
