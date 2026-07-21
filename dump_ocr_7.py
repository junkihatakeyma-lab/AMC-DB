import json

data = [
    {"request_no": "10064", "hinmei": "IF258S=0132 サニタリー白 (IF258/S=0132) 図KF32-18-2D"},
    {"request_no": "10065", "hinmei": "IF220=0500 (出荷時品名 CTIF220-0500)"},
    {"request_no": "10066", "hinmei": "IF402=0406D"},
    {"request_no": "10067", "hinmei": "IF400B=0560"},
    {"request_no": "10068", "hinmei": "4F247-1390 (図KF11-059-2)"},
    {"request_no": "10069", "hinmei": "5F130改5-1137 ベンチュリー一体型 (鉄図面P170650)"},
    {"request_no": "1007", "hinmei": "IF409=1507"},
    {"request_no": "10070", "hinmei": "IF253=0500"},
    {"request_no": "10071", "hinmei": "IF226=0500 (45山、上パッキンTR20) (図KF31-14-28-14)"},
    {"request_no": "10072", "hinmei": "IF100/225=0755"}
]

with open("parsed_7.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
