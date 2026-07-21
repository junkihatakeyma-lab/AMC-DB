import json

def generate_parsed_json():
    data = [
        {"request_no": "10222", "hinmei": "4F260-0600 (図KF17-174)"},
        {"request_no": "10223", "hinmei": "IF402/220=0406"},
        {"request_no": "10224", "hinmei": "IF226=0300 (45山、下パッキン) 図KF31-14-27-1"},
        {"request_no": "10225", "hinmei": "4F324-0915 試作"},
        {"request_no": "10226", "hinmei": "IF-130 (3-008349)"},
        {"request_no": "10227", "hinmei": "IF220F=0500"},
        {"request_no": "10228", "hinmei": "IF402B=0545"},
        {"request_no": "10229", "hinmei": "MT040 (5F210-0565)"},
        {"request_no": "1023", "hinmei": "IF223-0305 A"},
        {"request_no": "10230", "hinmei": "IF-119S (IF102-0500-052) 3-008125"},
        {"request_no": "10231", "hinmei": "IF-129 (IF100=0181)"},
        {"request_no": "10232", "hinmei": "IF253=1053 (図KF26-59-13)"},
        {"request_no": "10233", "hinmei": "IF220FF=1000 W型 Φ230"},
        {"request_no": "10234", "hinmei": "4F247-1390 (図KF11-059-2)"},
        {"request_no": "10235", "hinmei": "5F190-2055 試作"},
        {"request_no": "10236", "hinmei": "IF220=0500"},
        {"request_no": "10237", "hinmei": "IF433B=0660"},
        {"request_no": "10238", "hinmei": "IF253=0500"},
        {"request_no": "10239", "hinmei": "IF433B=0660 TF"},
        {"request_no": "1024", "hinmei": "3F200-1270 2ヶ入"},
        {"request_no": "10240", "hinmei": "IF226=0750 (図KF31-14-29-9)"},
        {"request_no": "10241", "hinmei": "SA400-25S (IF104=0400)"},
        {"request_no": "10242", "hinmei": "IF406=0630D (図KF28-12C-2)"},
        {"request_no": "10243", "hinmei": "83024380 (IF125A=0850C)"},
        {"request_no": "10244", "hinmei": "4F455-0800 (図KF29-258-3)"},
        {"request_no": "10245", "hinmei": "IF220-500-012 (MJT-005316-02)"},
        {"request_no": "10246", "hinmei": "IF220=0500"},
        {"request_no": "10247", "hinmei": "IF253E=0420 (4F200B/S-0420) 1.94m2 (図KF29-059-1)"},
        {"request_no": "10248", "hinmei": "FE2-253-OTR (IF400=0753=100)"},
        {"request_no": "10249", "hinmei": "IF258F=0450 (4F120A-0450) (図MH0673-002-02)"},
        {"request_no": "1025", "hinmei": "IF220-500-012 (MJT-005316-01)"},
        {"request_no": "10250", "hinmei": "IF220=0500"},
        {"request_no": "10251", "hinmei": "IF210=0100"},
        {"request_no": "10252", "hinmei": "IF210=0100"},
        {"request_no": "10253", "hinmei": "IF258F=0300 (4F090B-0300) オサメ工業50Aフェルール付(客先支給)"},
        {"request_no": "10254", "hinmei": "FE3-2000-OTF (IF426=2000)"},
        {"request_no": "10255", "hinmei": "脱水装置用フィルター 9m2 コーキング加工有"},
        {"request_no": "10256", "hinmei": "IF406=0630D (図KF28-12C-2)"},
        {"request_no": "10257", "hinmei": "4F200-0545 (図K18-194)"},
        {"request_no": "10258", "hinmei": "IF220=0500"},
        {"request_no": "10259", "hinmei": "IF400B=0560"},
        {"request_no": "1026", "hinmei": "IF406=0630B"},
        {"request_no": "10260", "hinmei": "4F162-0545 (100山)"},
        {"request_no": "10261", "hinmei": "IF253SW=0500A 変形サニタリー 内筒接着型(強化) (IF253/SW=0500A)"},
        {"request_no": "10262", "hinmei": "4F180-0500"},
        {"request_no": "10263", "hinmei": "ECOクリーン用 2連フィルター (IF426=1200 2連溶接型) (客先図番:WF0015-273-01) (AMC図番:KF31-302-2参照)"},
        {"request_no": "10264", "hinmei": "IF226=0300 (45山、上パッキン) 図KF31-14-27-1参考"},
        {"request_no": "10265", "hinmei": "IF226=0300 (66山、上パッキン) 図KF31-14-27-3参考"},
        {"request_no": "10266", "hinmei": "IF226=0300 (66山、上パッキン) 図KF31-14-27-3参考"},
        {"request_no": "10267", "hinmei": "B-516-2 パッキンなし、アース線付 (IF253C=0800)"}
    ]

    with open('parsed_5.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generate_parsed_json()
