import json

data = [
    {"request_no": "10463", "hinmei": "4F162-0545"},
    {"request_no": "10482", "hinmei": "4F180/162-0500"},
    {"request_no": "10483", "hinmei": "IF402B=0545 (図KF36-189)"},
    {"request_no": "10484", "hinmei": "IF-220C パッキンなし MJT-005316-05-N"},
    {"request_no": "10485", "hinmei": "IF-130 (3-008349)"},
    {"request_no": "10486", "hinmei": "IF220FF=0500 W型 φ230"},
    {"request_no": "10487", "hinmei": "IF220=0500"},
    {"request_no": "10488", "hinmei": "FE5-1400-0TF (4F455-1400) ハンガーH3タイプ (図KF29-258-4)"},
    {"request_no": "10489", "hinmei": "FE5-1700-0TF (4F455-1700) ハンガーH3タイプ (図KF29-258-5)"},
    {"request_no": "1049", "hinmei": "IF226=0500"},
    {"request_no": "10490", "hinmei": "5F183-1072"},
    {"request_no": "10491", "hinmei": "5F183-1072 (図KF22-225参考)"},
    {"request_no": "10492", "hinmei": "IF220FW=1000"},
    {"request_no": "10493", "hinmei": "IF433B=0660"},
    {"request_no": "10494", "hinmei": "5F132-2051"},
    {"request_no": "10495", "hinmei": "4F205-0624"},
    {"request_no": "10496", "hinmei": "IF258=0600 (図KF30-273-6参考)"},
    {"request_no": "10497", "hinmei": "4F205-0624"},
    {"request_no": "10498", "hinmei": "4F145B-0150 (0.75m2. PET. G2260-白, ナノファイバー(PAN 1g/m2) ) 図KF35-368参照"},
    {"request_no": "10499", "hinmei": "IF253=0750"}
]

with open('parsed_4.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
