import re
import codecs

with open('static/app2.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

text = re.sub(r'alert\([\s\S]*?\);', "alert('message');", text)
text = re.sub(r'prompt\([\s\S]*?\);', "prompt('newName');", text)
text = re.sub(r'innerText = [^\n]+', "innerText = 'error';", text)
text = re.sub(r'innerHTML = \'<div class="empty-state">.*?</div>\';', "innerHTML = '<div class=\"empty-state\">no results</div>';", text)
text = re.sub(r'statsContainer.textContent = `.*? \$\{totalHits\} .*?`;', "statsContainer.textContent = `Total ${totalHits} results`;", text)
text = re.sub(r'removeBtn\.innerText = \'.*?\';', "removeBtn.innerText = 'X';", text)

text = re.sub(r't = t.replace\(\/\[.*?\n.*?\{', r't = t.replace(/[A-Za-z0-9]/g, function(s) {', text)
text = re.sub(r't = t.replace\(\/\[.*?\/g, \'#\'\)\.replace\(\/\[.*?\/g, \'-\'\);', r"t = t.replace(/[＃]/g, '#').replace(/[ー−―‐]/g, '-');", text)


with open('static/app2.js', 'w', encoding='utf-8') as f:
    f.write(text)
