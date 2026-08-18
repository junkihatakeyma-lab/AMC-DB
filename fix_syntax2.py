import re
import codecs

with open('static/app2.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

text = re.sub(r"const pCode = p\.product_code \|\| '[^\n]+?;", "const pCode = p.product_code || 'Unknown';", text)
text = re.sub(r"if \(p\.name && p\.name !== '[^\n]+? && p\.name !== '[^\n]+?\)'\)", "if (p.name && p.name !== 'UnregisteredPart' && p.name !== 'UnregisteredProduct')", text)
text = re.sub(r"let isRedText = c\.role === '[^\n]+?;", "let isRedText = c.role === 'RedText';", text)
text = re.sub(r"let titleText = `[^\n]+?;", "let titleText = `Unclassified`;", text)

with open('static/app2.js', 'w', encoding='utf-8') as f:
    f.write(text)
