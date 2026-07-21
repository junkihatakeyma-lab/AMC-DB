import os
import glob
import sqlite3
import re
import urllib.request
import time
import subprocess

DB_PATH = '部品DB.sqlite'
HANDWRITTEN_DIR = 'data/加工依頼書_自動読取'

def import_new_handwritten():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 既に登録されている手書き依頼書のパスを取得
    c.execute("SELECT file FROM requests WHERE is_handwritten=1")
    existing_files = {row[0].replace('\\', '/') for row in c.fetchall()}
    
    # ディレクトリ内の全画像を検索
    if not os.path.exists(HANDWRITTEN_DIR):
        print(f"ディレクトリが見つかりません: {HANDWRITTEN_DIR}")
        return
        
    all_files = glob.glob(f"{HANDWRITTEN_DIR}/*.jpg") + glob.glob(f"{HANDWRITTEN_DIR}/*.png")
    new_files = [f for f in all_files if f.replace('\\', '/') not in existing_files]
    
    if not new_files:
        print("追加された新しい手書き依頼書はありませんでした。")
        return
        
    print(f"新しく {len(new_files)} 件の手書き依頼書が見つかりました。読み込みを開始します...")
    
    # OCRエンジンの読み込み (新しいファイルがある場合のみ)
    reader = None
    try:
        import easyocr
        print("OCRエンジンを準備中...")
        reader = easyocr.Reader(['ja', 'en'], gpu=False)
    except Exception as e:
        print(f"OCRエンジンの読み込みに失敗しました（文字は抽出されません）: {e}")
        
    for fp in new_files:
        filename = os.path.basename(fp)
        base_name = os.path.splitext(filename)[0]
        if base_name.startswith('#') or base_name.startswith('＃'):
            request_no = base_name[1:]
        else:
            request_no = base_name
            
        db_path = fp.replace('\\', '/')
        hinmei = ""
        
        # OCRで品名を抽出
        if reader:
            try:
                ocr_results = reader.readtext(fp, detail=0)
                ocr_text = "\n".join(ocr_results)
                match = re.search(r'品名[\s:：]*([^\n]+)', ocr_text)
                if match:
                    hinmei = match.group(1).strip()
            except Exception as e:
                print(f"{filename} のOCR読み取りエラー: {e}")
                
        # データベースに登録
        try:
            c.execute("""
                INSERT OR REPLACE INTO requests (request_no, seiban, hinmei, biko, file, issue_date, qty, kiji, yoto, noki_raw, noki, dest, spec, prev, is_handwritten)
                VALUES (?, ?, ?, ?, ?, '', '', '', '', '', '', '', '', '', 1)
            """, (request_no, '', hinmei, '', db_path))
            print(f"追加: {filename} (抽出された品名: {hinmei})")
        except Exception as e:
            print(f"{filename} のDB登録エラー: {e}")
            
    conn.commit()
    conn.close()

def main():
    print("="*50)
    print("部品DB データ更新ツール")
    print("="*50)
    
    # 1. Excelデータ、PDF、図面、検査証などの基本データ取り込み
    print("\n【1/4】エクセルや図面、PDFデータの更新を確認しています...")
    import import_data
    import_data.import_all()
    
    # 2. 新しい手書き画像の取り込みとOCR
    print("\n【2/4】新しい手書き依頼書画像の更新を確認しています...")
    import_new_handwritten()
    
    # 3. プレビュー画像の生成（図面、検査証などのプレビュー作成）
    print("\n【3/4】新しいファイルのプレビュー画像を作成しています...")
    import generate_previews
    generate_previews.main()
    
    # 4. サーバーのキャッシュを更新して画面に即座に反映
    print("\n【4/4】画面のデータを最新状態に更新しています...")
    try:
        req = urllib.request.Request('http://localhost:8000/api/reload_cache')
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print("サーバーのデータ更新に成功しました！")
    except Exception as e:
        print("※ サーバーが起動していないか、更新通知に失敗しました。サーバー起動後に最新データが読み込まれます。")
        
    print("\n" + "="*50)
    print("🎉 すべてのデータ更新作業が完了しました！")
    print("ブラウザを更新（F5）して最新の検索画面をご確認ください。")
    print("="*50)
    
    # Windowsでダブルクリック実行した場合にすぐ閉じないようにする
    time.sleep(3)

if __name__ == '__main__':
    main()
