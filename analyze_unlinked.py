import sqlite3
import re
from collections import Counter

conn = sqlite3.connect('部品DB.sqlite')
c = conn.cursor()

c.execute('''
    SELECT DISTINCT part_no
    FROM bom_components
    WHERE part_no IS NOT NULL AND part_no != ''
      AND role != 'ラベル' AND role != '【特記・赤字】'
      AND part_no NOT IN (SELECT db_part_no FROM part_master_links)
''')
unlinked = [r[0] for r in c.fetchall()]
conn.close()

patterns = {
    'Full-width characters (全角英数/記号)': r'[！-～]', # Full width ASCII
    'Multiple spaces (連続スペース)': r'\s{2,}',
    'Full-width space (全角スペース)': r'　',
    'Starts/Ends with space (前後の空白)': r'^\s|\s$',
    'Various hyphens (ハイフンの揺れ: ー, ‐, ‑, ‒, –, —, ―)': r'[ー‐‑‒–—―]',
    'Full-width parentheses (全角括弧)': r'[（）]',
    'Potential OCR error I/1, O/0 (OCRの誤読疑い)': r'(?:O0|0O|I1|1I|l1|1l)',
}

results = {k: [] for k in patterns}

for p in unlinked:
    for k, pat in patterns.items():
        if re.search(pat, p):
            results[k].append(p)

with open('unlinked_analysis.txt', 'w', encoding='utf-8') as f:
    f.write(f"Total unlinked parts: {len(unlinked)}\n\n")
    for k, items in results.items():
        f.write(f"--- {k} ({len(items)} items) ---\n")
        f.write("\n".join(items[:20]))
        if len(items) > 20:
            f.write(f"\n... and {len(items)-20} more\n")
        f.write("\n\n")
