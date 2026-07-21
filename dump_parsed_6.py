import json

data = [
    {
        "request_no": "10516",
        "hinmei": "脱水乾燥装置用フィルター 1.56m2 (図面:BS0868-600-01(内筒) ↓=BS0868-601-01(アウター))"
    },
    {
        "request_no": "10517",
        "hinmei": "KTEF66-BHS (IF220=0529H) ホーコス図番PN25242CA00110 AMC図番KF22-223"
    },
    {
        "request_no": "10518",
        "hinmei": "4F170-0752 (図KF31-297)"
    },
    {
        "request_no": "10519",
        "hinmei": "83025585 (IF125A=1200C(42山))"
    },
    {
        "request_no": "1052",
        "hinmei": "IF226=0345 E6100"
    },
    {
        "request_no": "10520",
        "hinmei": "IF253C=0500"
    },
    {
        "request_no": "10521",
        "hinmei": "5F137H-1050"
    },
    {
        "request_no": "10522",
        "hinmei": "IF400'=0450 内筒熔接金網用"
    },
    {
        "request_no": "10523",
        "hinmei": "4F145B-0300 (1m2, PET, G2260-B, TIファイバー(PAN 1g/m2)) 図KF35-368-1"
    },
    {
        "request_no": "10524",
        "hinmei": "4F220-0250 (図KF31-288)"
    },
    {
        "request_no": "10525",
        "hinmei": "IF220FW=1000"
    },
    {
        "request_no": "10526",
        "hinmei": "5F130改5-1137ベンチュリー一体型 (客先図番P169459)"
    },
    {
        "request_no": "10527",
        "hinmei": "4F162-0805"
    },
    {
        "request_no": "10528",
        "hinmei": "耐熱6K-2000L (3F136.6-2051)"
    },
    {
        "request_no": "10529",
        "hinmei": "IF253E=0420(4F200B/S-0420) 1.94m2 (図KF29-059-1)"
    },
    {
        "request_no": "1053",
        "hinmei": "4F162-0805"
    },
    {
        "request_no": "10530",
        "hinmei": "IF433B=0660 TF EPDM"
    },
    {
        "request_no": "10531",
        "hinmei": "MBR320×300+01 TR(5F320-0320) 底溶着二重"
    },
    {
        "request_no": "10532",
        "hinmei": "3F162/100-0545 60山"
    },
    {
        "request_no": "10533",
        "hinmei": "IF406=0630P (図KF28-12C-2)"
    }
]

with open('parsed_6.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("dumped to parsed_6.json")
