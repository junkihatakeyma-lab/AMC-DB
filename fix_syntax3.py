import re
import codecs

with open('static/app2.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

text = text.replace("(p.name === 'Unregistered')') ?", "(p.name === 'Unregistered') ?")

with open('static/app2.js', 'w', encoding='utf-8') as f:
    f.write(text)
