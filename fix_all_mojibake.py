import codecs

with codecs.open('static/app.js', 'r', 'utf-8') as f:
    content = f.read()

replacements = {
    'E剥 髢E騾E讀懈渊險E': '📋 関連検査証',
    '莉ｶ': '件',
    '繝励Ξ繝薙Η繝ｼ': 'プレビュー',
    'E倹 繝悶Λ繧E繧E縺E髢九￥': '🌐 ブラウザで開く',
    '髢九￥': '開く',
    'E胴 髢E騾E蜀咏悄繝ｻ縺昴・莉E': '📸 関連写真・その他',
    'E盁E髢E騾E蝗ｳ髱E': '📐 関連図面',
    '繝ｭ繝ｼ繧E繝ｫ縺E髢九￥': 'ローカルで開く',
    'E搭 BOM荳€隕ｧ': '📦 BOM一覧',
    '蠖ｹ蜑ｲ': '役割',
    '驛ｨ蜩∫刁EE': '部品番号',
    '莉墓ｧ倥Γ繝｢': '仕様メモ',
    '陬E逡E': '製番',
    '蜩∝錐': '品名',
    'Excel繧帝幕縺・: 'Excelを開く',
    'E剥 讀懈渊險E荳€隕ｧ': '📋 検査証一覧',
    'E胴 蜀咏悄繝ｻ縺昴・莉紋ｸ€隕ｧ': '📸 写真・その他一覧',
    '髢E騾E陬E蜩・: '関連製品:',
    'E盁E蝗ｳ髱E荳€隕ｧ': '📐 図面一覧',
    '繝€繧E繝ｳ繝ｭ繝ｼ繝E/ 髢九￥': 'ダウンロード / 開く',
    '繝Eぉ繝Eけ縺輔ｌ縺滁E・岼縺E隧E蠖薙☁E九ョ繝ｼ繧E縺後≠繧翫∪縺帙ａE': 'チェックされた項目に該当するデータがありません',
    '繝励Ξ繝薙Η繝ｼ逕ｻ蜒上′縺めE縺E縺帙ｓE・DF螟画鋤蠕E■縲√∪縺溘E譛ｪ逕滓E縺E縺呻E・': 'プレビュー画像がありません（PDF変換待ち、または未生成です）',
    '侁E ': '追加の ',
    '✁E': '✖',
    '⚠E': '⚠️',
    '手書ぁE要確誁E': '手書き(要確認)',
    '✍︁E': '✍️ '
}

for k, v in replacements.items():
    content = content.replace(k, v)

# Fix edge case "E/ 髢九￥" mapping issue
content = content.replace('ダウンロード / 開く</a>', 'ダウンロード / 開く</a>')

with codecs.open('static/app.js', 'w', 'utf-8') as f:
    f.write(content)

print("Mojibake cleaned successfully!")
