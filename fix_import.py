import re

with open('import_parts_master.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_func = """def normalize(text):
    if not isinstance(text, str):
        return ""
    text = text.upper()
    text = re.sub(r'[^A-Z0-9]', '', text)
    return text"""

new_func = """import unicodedata

def normalize(text):
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize('NFKC', text)
    text = text.upper()
    text = re.sub(r'[^A-Z0-9]', '', text)
    return text"""

if old_func in text:
    text = text.replace(old_func, new_func)
    with open('import_parts_master.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated import_parts_master.py")
else:
    print("Function not found!")
