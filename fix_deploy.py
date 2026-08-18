import re

try:
    with open('deploy_to_firebase.py', 'r', encoding='shift_jis') as f:
        content = f.read()
except:
    with open('deploy_to_firebase.py', 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

# Fix the broken zenkaku string
content = re.sub(r"text = text\.translate\(str\.maketrans\([\s\S]*?'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'\n    \)\)", '''text = text.translate(str.maketrans(
        'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ０１２３４５６７８９',
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    ))''', content)

# PowerShell replaced '' with some garbage if we don't handle it, but it might just be the zenkaku strings.
# Wait, let's fix any broken strings if there's mojibake in the print statements.
content = content.replace("fvCĂ܂...", "デプロイしています...")
content = content.replace("fvCɎs܂B", "デプロイに失敗しました。")
content = content.replace("fvCɎ܂B", "デプロイに成功しました。")
content = content.replace("data/H˗_?E", "data/加工依頼書_手書き")
content = content.replace("data/H˗", "data/加工依頼書")
content = content.replace("data/H˗_", "data/加工依頼書_手書き")
content = content.replace("H˗", "加工依頼書")

# Save as UTF-8
with open('deploy_to_firebase.py', 'w', encoding='utf-8') as f:
    f.write(content)
