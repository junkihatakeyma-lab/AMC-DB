import os

try:
    with open('templates/index.html', 'r', encoding='cp932') as f:
        content = f.read()
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed encoding of index.html to utf-8")
except Exception as e:
    print("Error:", e)
