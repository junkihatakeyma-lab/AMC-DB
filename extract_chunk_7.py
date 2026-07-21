import json

data = [
    {"request_no": "10534", "hinmei": "4F170-0752 (図KF31-297)"},
    {"request_no": "10535", "hinmei": "IF220FF/5F230=0450"},
    {"request_no": "10536", "hinmei": "IF220=0500 (出荷時品名 CTIF220-0500Z)"},
    {"request_no": "10537", "hinmei": "4F170A-104-1765-A (KF37-427)"},
    {"request_no": "10538", "hinmei": "フィルター組立 (4F325-0625) φ325×625H"},
    {"request_no": "10539", "hinmei": "IF220E=0500"},
    {"request_no": "1054", "hinmei": "IF100M=0500TF"},
    {"request_no": "10540", "hinmei": "IF220=0730 (56山) (図KF41-059)"},
    {"request_no": "10541", "hinmei": "FE5-1700-OTF (4F455-1700) ハンガーH3タイプ (図KF29-258-6)"},
    {"request_no": "10542", "hinmei": "FE5-1700-OTF (4F455-1700) ハンガーH3タイプ (図KF29-258-5)"},
    {"request_no": "10543", "hinmei": "IF220=0500"},
    {"request_no": "10544", "hinmei": "IF220=1000B"},
    {"request_no": "10545", "hinmei": "6K 2000L (3F136.6-2000 (2051))"},
    {"request_no": "10546", "hinmei": "6K 1800L (3F136.6-1800(1851)) (図KF22-195-5-3)"},
    {"request_no": "10547", "hinmei": "IF253SW=0500A 変形サニタリー 内筒接着型(強化) (IF253/SW=0500A)"},
    {"request_no": "10548", "hinmei": "KTEF66-BHS (IF220=0529H) ホーコス図番 PN25242CA00110 AMC図番 KF22-223"},
    {"request_no": "10549", "hinmei": "KTEF66-UB (IF220FF=0632) (客先図番 PN36072CA00110)"},
    {"request_no": "1055", "hinmei": "5F192-1000 新(クマクラ型)"},
    {"request_no": "10550", "hinmei": "4F162-0805"},
    {"request_no": "10551", "hinmei": "3F136-0851 (図KF25-195-8)"}
]

with open('parsed_7.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
