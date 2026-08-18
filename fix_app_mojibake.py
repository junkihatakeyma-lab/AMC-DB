import codecs

replacements = {
    '【特記E赤字、E': '【特記・赤字】',
    '例外レイアウトE確認渁E': '例外レイアウト・確認済',
    '例外レイアウトE要確誁E': '例外レイアウト・要確認',
    '✍︁E加工依頼書_BOM一佁E': '✍️ 加工依頼書_BOM一体',
    '✍︁E': '✍️',
    '⚠E': '⚠️',
    '数釁E': '数量',
    '用送E': '用途',
    '出荷允E': '出荷先',
    '備老E': '備考',
    '仕槁E': '仕様',
    '品名を編雁E': '品名を編集',
    '允EEファイルを開ぁE': '元ファイルを開く'
}

with codecs.open('static/app.js', 'r', 'utf-8') as f:
    content = f.read()

for bad, good in replacements.items():
    content = content.replace(bad, good)

with codecs.open('static/app.js', 'w', 'utf-8') as f:
    f.write(content)

print("Mojibake fixed in app.js!")
