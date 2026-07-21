import re

with open('static/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Update addPartInput to enforce max 5
old_add = """window.addPartInput = function(val = '') {
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
};"""

new_add = """window.addPartInput = function(val = '') {
    const list = document.getElementById('partInputsList');
    const currentInputs = list.querySelectorAll('.part-input-row');
    if (currentInputs.length >= 5) {
        alert('部品番号の検索窓は最大5つまでです。');
        return;
    }

    const row = document.createElement('div');
    row.className = 'part-input-row';
    row.style = 'display: flex; gap: 4px; flex: 1;';
    
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'searchPartInput';
    input.placeholder = '追加の部品番号';
    input.value = val;
    input.style = 'width: 100%;';
    input.addEventListener('input', () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(performSearch, 300);
    });
    
    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.className = 'btn btn-secondary';
    removeBtn.innerText = '✖';
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
};"""

content = content.replace(old_add, new_add)

# Make sure clearAllSearch resets the button
old_clear = """        document.querySelector('.searchPartInput').addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(performSearch, 300);
        });
    }
    performSearch();
};"""
new_clear = """        document.querySelector('.searchPartInput').addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(performSearch, 300);
        });
        document.getElementById('addPartBtn').disabled = false;
    }
    performSearch();
};"""
content = content.replace(old_clear, new_clear)

# Update triggerTagSearch
old_trigger = """        const list = document.getElementById('partInputsList');
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
        }"""
new_trigger = """        const list = document.getElementById('partInputsList');
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
        }"""
content = content.replace(old_trigger, new_trigger)

with open('static/app.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated app.js for 5 window limit")
