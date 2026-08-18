import re

with open('static/app_raw.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the statsContainer assignment and array slicing
old_stats = "statsContainer.textContent = `全体で ${totalHits} 件ヒットしました`;"

new_stats = """statsContainer.textContent = `全体で ${totalHits} 件ヒットしました${totalHits > 500 ? ' (結果が多すぎるため、各カテゴリ上位100件のみ表示しています)' : ''}`;

    let origBomsLen = allBoms.length;
    let origReqsLen = allReqs.length;
    let origInspsLen = allInsps.length;
    let origPhotosLen = allPhotos.length;
    let origDrawingsLen = allDrawings.length;

    allBoms = allBoms.slice(0, 100);
    allReqs = allReqs.slice(0, 100);
    allInsps = allInsps.slice(0, 100);
    allPhotos = allPhotos.slice(0, 100);
    allDrawings = allDrawings.slice(0, 100);
"""
text = text.replace(old_stats, new_stats)

# Replace the headers to show the original counts
text = text.replace('<h3>📋 BOM一覧 (${allBoms.length}件)</h3>', '<h3>📋 BOM一覧 (${allBoms.length}件表示 / 全${origBomsLen}件中)</h3>')
text = text.replace('<h3>📄 加工依頼書一覧 (${allReqs.length}件)</h3>', '<h3>📄 加工依頼書一覧 (${allReqs.length}件表示 / 全${origReqsLen}件中)</h3>')
text = text.replace('<h3>🔍 検査証一覧 (${allInsps.length}件)</h3>', '<h3>🔍 検査証一覧 (${allInsps.length}件表示 / 全${origInspsLen}件中)</h3>')
text = text.replace('<h3>📷 写真・その他一覧 (${allPhotos.length}件)</h3>', '<h3>📷 写真・その他一覧 (${allPhotos.length}件表示 / 全${origPhotosLen}件中)</h3>')
text = text.replace('<h3>📐 図面一覧 (${allDrawings.length}件)</h3>', '<h3>📐 図面一覧 (${allDrawings.length}件表示 / 全${origDrawingsLen}件中)</h3>')

with open('static/app_raw.js', 'w', encoding='utf-8-sig') as f:
    f.write(text)

print("Patched app_raw.js successfully.")
