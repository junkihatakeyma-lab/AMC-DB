import sqlite3
import json

def check_suspicious():
    conn = sqlite3.connect('C:/Users/jhatakeyama/.gemini/antigravity/scratch/PartsSearchDB/部品DB.sqlite')
    c = conn.cursor()

    c.execute("SELECT request_no, hinmei FROM requests WHERE hinmei LIKE '[手書き]%'")
    all_ocr = c.fetchall()

    skipped = []
    suspicious = []

    for req_no, hinmei in all_ocr:
        val = hinmei.replace('[手書き]', '').strip()
        if not val or val == 'なし' or val == '不明' or val == '?' or val == '？':
            skipped.append((req_no, hinmei))
        elif len(val) <= 2:
            suspicious.append((req_no, hinmei))

    print(f'Total OCR items: {len(all_ocr)}')
    print(f'Skipped/Empty: {len(skipped)}')
    print(f'Suspicious (very short): {len(suspicious)}')

    print('\n--- Skipped/Empty ---')
    for r, h in skipped[:10]:
        print(f'  req_no: {r}')

    print('\n--- Suspicious (<= 2 chars) ---')
    for r, h in suspicious[:10]:
        print(f'  req_no: {r} -> {h}')

if __name__ == "__main__":
    check_suspicious()
