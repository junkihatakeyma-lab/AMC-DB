with open('static/app2.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m1 = re.search(r'window\.openLinkModal[\s\S]*?window\.saveLinkModal[\s\S]*?\}', text)
if m1:
    print("--- Modals ---")
    print(m1.group(0))

m2 = re.search(r'<td>\$\{createTag\(c\.part_no, \'part\'\)\}.*?</td>', text)
if m2:
    print("--- HTML rendering ---")
    print(m2.group(0))

