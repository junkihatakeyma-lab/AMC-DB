with open('static/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(r"\'/\'", "'/'")
content = content.replace(r"\'\')", "'')")

with open('static/app.js', 'w', encoding='utf-8') as f:
    f.write(content)
