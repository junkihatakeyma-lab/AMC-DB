import json
import os

data = {
  'data/BOM\\IF226-0500 66山(#13598 PPSー裏SUS アマノメンテ).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF226-101', 'note': 'φ187*φ70, (140g)'},
    {'role': 'プレートB', 'part_no': 'IF100-102', 'note': 'φ154*φ70/0'},
    {'role': 'プレートB ASSY', 'part_no': 'IF100-102 ASSY A', 'note': 'φ154+WEB付き'},
    {'role': 'チューブ', 'part_no': 'IF226-104-0500-A', 'note': 'SUS304 6*8, t0.6*500*265L(φ82)'},
    {'role': 'リテーナー', 'part_no': 'IF226-110', 'note': 'φ80.5*9'},
    {'role': 'Ｌ字', 'part_no': 'IF226-113', 'note': '×3'},
    {'role': 'チューブASSY酸洗い済品', 'part_no': 'IF226-104-0500-A-SA', 'note': ''},
    {'role': 'プレートB ASSY (2)', 'part_no': 'IF100-102 ASSY A-BF0300', 'note': '(150g)'},
    {'role': '接着剤', 'part_no': 'KB-400', 'note': ''},
    {'role': 'ロックナット', 'part_no': 'IF000-LN/', 'note': 'M8SUS'},
    {'role': 'ウェルドボルト', 'part_no': 'IF000-WEB/', 'note': 'M8-20SUS'},
    {'role': 'Ｐ／Ｋ', 'part_no': 'IF226-007B-EPDM-10-S', 'note': 'EPDM t10*φ187*φ155'},
    {'role': '外装箱', 'part_no': 'IF226-0500', 'note': '（4ヶ入りSカートン・仕切り付）'}
  ],
  'data/BOM\\IF226-0500(#12941).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF226-101', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF100-102', 'note': ''},
    {'role': 'プレートB ASSY', 'part_no': 'IF100-102 ASSY A', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF226-104-0500-A', 'note': ''},
    {'role': 'リテーナー', 'part_no': 'IF226-110', 'note': ''},
    {'role': 'Ｌ字', 'part_no': 'IF226-113', 'note': ''},
    {'role': 'チューブASSY酸洗い済品', 'part_no': 'IF226-104-0500-A-SA', 'note': ''},
    {'role': 'プレートB ASSY (2)', 'part_no': 'IF100-102 ASSY A-BF0300', 'note': ''},
    {'role': 'ロックナット', 'part_no': 'IF000-LN/', 'note': ''},
    {'role': 'ウェルドボルト', 'part_no': 'IF000-WEB/', 'note': ''},
    {'role': 'Ｐ／Ｋ', 'part_no': 'IF226-007B-EPDM-10-S', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF226-0500', 'note': ''}
  ],
  'data/BOM\\IF226-0500(#12946).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF226-101', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF100-102', 'note': ''},
    {'role': 'プレートB ASSY', 'part_no': 'IF100-102 ASSY A', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF226-104-0500-A', 'note': ''},
    {'role': 'リテーナー', 'part_no': 'IF226-110', 'note': ''},
    {'role': 'Ｌ字', 'part_no': 'IF226-113', 'note': ''},
    {'role': 'チューブASSY酸洗い済品', 'part_no': 'IF226-104-0500-A-SA', 'note': ''},
    {'role': 'プレートB ASSY (2)', 'part_no': 'IF100-102 ASSY A-BF0300', 'note': ''},
    {'role': 'ロックナット', 'part_no': 'IF000-LN/', 'note': ''},
    {'role': 'ウェルドボルト', 'part_no': 'IF000-WEB/', 'note': ''},
    {'role': 'Ｐ／Ｋ', 'part_no': 'IF226-007B-EPDM-10-S', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF226-0500', 'note': ''}
  ],
  'data/BOM\\IF226-0500(#12948 酸洗い佐藤電化).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF226-101', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF100-102', 'note': ''},
    {'role': 'プレートB ASSY', 'part_no': 'IF100-102 ASSY A', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF226-104-0500-A', 'note': ''},
    {'role': 'リテーナー', 'part_no': 'IF226-110', 'note': ''},
    {'role': 'Ｌ字', 'part_no': 'IF226-113', 'note': ''},
    {'role': 'チューブASSY酸洗い済品', 'part_no': 'IF226-104-0500-A-SA', 'note': ''},
    {'role': 'プレートB ASSY (2)', 'part_no': 'IF100-102 ASSY A-BF0300', 'note': ''},
    {'role': 'ロックナット', 'part_no': 'IF000-LN/', 'note': ''},
    {'role': 'ウェルドボルト', 'part_no': 'IF000-WEB/', 'note': ''},
    {'role': 'Ｐ／Ｋ', 'part_no': 'IF226-007B-SI-WH-10-S', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF226-0500', 'note': ''}
  ],
  'data/BOM\\IF226-0500(#13833 EPDM 白).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF226-101', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF100-102', 'note': ''},
    {'role': 'プレートB ASSY', 'part_no': 'IF100-102 ASSY A', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF226-104-0500', 'note': ''},
    {'role': 'リテーナー', 'part_no': 'IF226-110', 'note': ''},
    {'role': 'Ｌ字', 'part_no': 'IF226-113', 'note': ''},
    {'role': 'チューブASSY酸洗い済品', 'part_no': 'IF226-104-0500-A-SA', 'note': ''},
    {'role': 'プレートB ASSY (2)', 'part_no': 'IF100-102 ASSY A-BF0300', 'note': ''},
    {'role': 'ロックナット', 'part_no': 'IF000-LN/', 'note': ''},
    {'role': 'ウェルドボルト', 'part_no': 'IF000-WEB/', 'note': ''},
    {'role': 'Ｐ／Ｋ', 'part_no': 'IF226-007B-EPDM-10-W', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF226-0500', 'note': ''}
  ],
  'data/BOM\\IF226-0500(#13912 KS400 PPS-SUS 酸洗い).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF226-101', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF100-102', 'note': ''},
    {'role': 'プレートB ASSY', 'part_no': 'IF100-102 ASSY A', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF226-104-0500-A', 'note': ''},
    {'role': 'リテーナー', 'part_no': 'IF226-110', 'note': ''},
    {'role': 'Ｌ字', 'part_no': 'IF226-113', 'note': ''},
    {'role': 'チューブASSY酸洗い済品', 'part_no': 'IF226-104-0500-A-SA', 'note': ''},
    {'role': 'プレートB ASSY (2)', 'part_no': 'IF100-102 ASSY A-BF0300', 'note': ''},
    {'role': 'ロックナット', 'part_no': 'IF000-LN/', 'note': ''},
    {'role': 'ウェルドボルト', 'part_no': 'IF000-WEB/', 'note': ''},
    {'role': 'Ｐ／Ｋ', 'part_no': 'IF226-007B-SI-WH-10-S', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF226-0500', 'note': ''}
  ],
  'data/BOM\\IF226-0500(#14041 酸洗い佐藤電化 接着剤ｼﾘｺﾝ).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF226-101', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF100-102', 'note': ''},
    {'role': 'プレートB ASSY', 'part_no': 'IF100-102 ASSY A', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF226-104-0500-A', 'note': ''},
    {'role': 'リテーナー', 'part_no': 'IF226-110', 'note': ''},
    {'role': 'Ｌ字', 'part_no': 'IF226-113', 'note': ''},
    {'role': 'チューブASSY酸洗い済品', 'part_no': 'IF226-104-0500-A-SA', 'note': ''},
    {'role': 'プレートB ASSY (2)', 'part_no': 'IF100-102 ASSY A-BF0300', 'note': ''},
    {'role': 'ロックナット', 'part_no': 'IF000-LN/', 'note': ''},
    {'role': 'ウェルドボルト', 'part_no': 'IF000-WEB/', 'note': ''},
    {'role': 'Ｐ／Ｋ', 'part_no': 'IF226-007B-SI-WH-10-S', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF226-0500', 'note': ''}
  ],
  'data/BOM\\IF226-0500(#3360②.3865.7607.8003.9312.12127.12838.2604-0135).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF226-001', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF100-402-045', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF100-004-0500', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF100-004-0500-A', 'note': ''},
    {'role': 'P/K', 'part_no': 'IF226-007A', 'note': ''},
    {'role': 'P/K', 'part_no': 'IF226-007B', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF100-0500A(内)', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF100M-0500TF', 'note': ''},
    {'role': 'メッシュ', 'part_no': 'IF100-009', 'note': ''}
  ],
  'data/BOM\\IF226-0750(#12943).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF226-101', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF100-102', 'note': ''},
    {'role': 'プレートB ASSY', 'part_no': 'IF100-102 ASSY A', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF226-104-0750-A', 'note': ''},
    {'role': 'リテーナー', 'part_no': 'IF226-110', 'note': ''},
    {'role': 'Ｌ字', 'part_no': 'IF226-113', 'note': ''},
    {'role': 'チューブASSY酸洗い済品', 'part_no': 'IF226-104-0750-A-SA', 'note': ''},
    {'role': 'プレートB ASSY (2)', 'part_no': 'IF100-102 ASSY A-BF0300', 'note': ''},
    {'role': 'ロックナット', 'part_no': 'IF000-LN/', 'note': ''},
    {'role': 'ウェルドボルト', 'part_no': 'IF000-WEB/', 'note': ''},
    {'role': 'Ｐ／Ｋ', 'part_no': 'IF226-007B-EPDM-10-S', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF226-0750', 'note': ''}
  ],
  'data/BOM\\IF226-0750(#13239 シリコンPK、KB-400、白TF).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF226-101', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF100-102', 'note': ''},
    {'role': 'プレートB ASSY', 'part_no': 'IF100-102 ASSY A', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF226-104-0750-A', 'note': ''},
    {'role': 'リテーナー', 'part_no': 'IF226-110', 'note': ''},
    {'role': 'Ｌ字', 'part_no': 'IF226-113', 'note': ''},
    {'role': 'チューブASSY酸洗い済品', 'part_no': 'IF226-104-0750-A-SA', 'note': ''},
    {'role': 'プレートB ASSY (2)', 'part_no': 'IF100-102 ASSY A-BF0300', 'note': ''},
    {'role': 'ロックナット', 'part_no': 'IF000-LN/', 'note': ''},
    {'role': 'ウェルドボルト', 'part_no': 'IF000-WEB/', 'note': ''},
    {'role': 'Ｐ／Ｋ', 'part_no': 'IF100-007-SI-S-A', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF226-0750', 'note': ''}
  ],
  'data/BOM\\IF226-0750(#13599　PPS-裏SUSTF ﾊﾝｶﾞｰH3).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF226-101', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF100-102', 'note': ''},
    {'role': 'プレートB ASSY', 'part_no': 'IF100-102 ASSY A', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF226-104-0750-A', 'note': ''},
    {'role': 'リテーナー', 'part_no': 'IF226-110', 'note': ''},
    {'role': 'Ｌ字', 'part_no': 'IF226-113', 'note': ''},
    {'role': 'チューブASSY酸洗い済品', 'part_no': 'IF226-104-0750-A-SA', 'note': ''},
    {'role': 'プレートB ASSY (2)', 'part_no': 'IF100-102 ASSY A-BF0300', 'note': ''},
    {'role': 'ロックナット', 'part_no': 'IF000-LN/', 'note': ''},
    {'role': 'ウェルドボルト', 'part_no': 'IF000-WEB/', 'note': ''},
    {'role': 'Ｐ／Ｋ', 'part_no': 'IF226-007B-EPDM-10-S', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF226-0750', 'note': ''}
  ],
  'data/BOM\\IF226-0750(#13689 EPDM　白).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF226-101', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF100-102', 'note': ''},
    {'role': 'プレートB ASSY', 'part_no': 'IF100-102 ASSY A', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF226-104-0750-A', 'note': ''},
    {'role': 'リテーナー', 'part_no': 'IF226-110', 'note': ''},
    {'role': 'Ｌ字', 'part_no': 'IF226-113', 'note': ''},
    {'role': 'チューブASSY酸洗い済品', 'part_no': 'IF226-104-0750-A-SA', 'note': ''},
    {'role': 'プレートB ASSY (2)', 'part_no': 'IF100-102 ASSY A-BF0300', 'note': ''},
    {'role': 'ロックナット', 'part_no': 'IF000-LN/', 'note': ''},
    {'role': 'ウェルドボルト', 'part_no': 'IF000-WEB/', 'note': ''},
    {'role': 'Ｐ／Ｋ', 'part_no': 'IF226-007B-EPDM-10-W', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF226-0750', 'note': ''}
  ],
  'data/BOM\\IF226-1000(#13601 首上ALL首下ﾊﾟｯｷﾝ無し).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF226-001', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF100-402-045', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF000-304-2000-80-S', 'note': ''},
    {'role': 'P/K', 'part_no': 'IF226-007A', 'note': ''},
    {'role': 'P/K', 'part_no': 'IF226-007B', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF220-1000（内）', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF226-1000', 'note': ''},
    {'role': 'メッシュ', 'part_no': 'IF100-009', 'note': ''}
  ],
  'data/BOM\\IF226-1500(#13602 首上ALL首下ﾊﾟｯｷﾝ無し).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF226-001', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF100-402-045', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF226-004-1500-A', 'note': ''},
    {'role': 'P/K', 'part_no': 'IF226-007A', 'note': ''},
    {'role': 'P/K', 'part_no': 'IF226-007B', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF226-1500', 'note': ''},
    {'role': 'メッシュ', 'part_no': 'IF100-009', 'note': ''}
  ],
  'data/BOM\\IF231-1500(#13430 耐熱 脱落防止 PPS-TF).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF231-101', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF231-102B', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF231-104-1500-A', 'note': ''},
    {'role': 'Ｐ／Ｋ', 'part_no': 'IF000-007/10-10-SI-W-S', 'note': ''},
    {'role': 'バー', 'part_no': 'IF231-111', 'note': ''},
    {'role': 'L字', 'part_no': 'IF231-113', 'note': ''},
    {'role': 'PPSリボン', 'part_no': 'IF000-008/25-0４50-PPS303-S', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF100-0500A(内)', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF231-1500', 'note': ''}
  ],
  'data/BOM\\IF253-1053(#12630.2604-0131).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF253-001', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF220-402-066', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF253-004-1053A', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF253-004-1053A-A', 'note': ''},
    {'role': 'P/K', 'part_no': 'IF220-007G', 'note': ''},
    {'role': 'P/K', 'part_no': 'IF220-007A', 'note': ''},
    {'role': 'P/K', 'part_no': 'IF220-007B-03', 'note': ''},
    {'role': 'P/K', 'part_no': 'IF220-007B-02', 'note': ''},
    {'role': 'ベンチュリー', 'part_no': 'IF253-014', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF253-1053', 'note': ''},
    {'role': 'メッシュ', 'part_no': 'IF220-009', 'note': ''}
  ],
  'data/BOM\\IF253-SW-0500(#13885.2605-0053).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF253-001', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF253/SW-902-066', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF253-004-0500A', 'note': ''},
    {'role': 'P/K', 'part_no': 'IF220-007A-DO-S', 'note': ''},
    {'role': 'ベンチュリー', 'part_no': 'IF253-014', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF220-0500（内）', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF220-0500（外）', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF220-0500', 'note': ''}
  ],
  'data/BOM\\IF253-SW-0500A(#13788.2605-0037).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF253-001', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF253/SW-902-066', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF253/SW-004-0500A', 'note': ''},
    {'role': 'ベンチュリー', 'part_no': 'IF253-014', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF220-0500（内）', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF220-0500', 'note': ''}
  ],
  'data/BOM\\IF253C-0800C(#14010 , 2605-0006).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF253C-001', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF220-402-066', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF253C-004-0800', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF253C-004-0800-A', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF220-004-1000', 'note': ''},
    {'role': 'ベンチュリー', 'part_no': 'IF253-014', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF253C-0800（内）', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF253C-0800', 'note': ''},
    {'role': 'メッシュ', 'part_no': 'IF220-009', 'note': ''}
  ],
  'data/BOM\\IF253C-1200(#13134.2605-0074 高さ違い).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF253C-001', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF220-402-066', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF253C-004-1200-A', 'note': ''},
    {'role': 'ベンチュリー', 'part_no': 'IF253-014', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF253C-1200（内）', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF253C-1200', 'note': ''},
    {'role': 'メッシュ', 'part_no': 'IF220-009', 'note': ''}
  ],
  'data/BOM\\IF253D-1000(KB-400#13997.2605-0098).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF253D-001P', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF220-002', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF253D-004-1000-A', 'note': ''},
    {'role': 'P/K', 'part_no': 'IF220-007D', 'note': ''},
    {'role': 'ベンチュリー', 'part_no': 'IF253-014', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF220-1000（内）', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF220-1000', 'note': ''}
  ],
  'data/BOM\\IF253D-1000(KB-400+E-6100#13372.2605-0115).xlsx': [
    {'role': 'プレートA', 'part_no': 'IF253D-001P', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF220-002', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF253D-004-1000', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF253D-004-1000-A', 'note': ''},
    {'role': 'P/K', 'part_no': 'IF220-007D-DO-S', 'note': ''},
    {'role': 'ベンチュリー', 'part_no': 'IF253-014', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF220-1000（内）', 'note': ''},
    {'role': '外装箱', 'part_no': 'IF220-1000', 'note': ''}
  ],
  'data/BOM\\IF258-S-0180(#13454.2606-0003).xlsx': [
    {'role': 'プレートA ASSY', 'part_no': 'IF258-101ASSY-HR', 'note': ''},
    {'role': 'プレートB', 'part_no': 'φ90/0　20/0', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF258-104-0180', 'note': ''},
    {'role': '外装箱', 'part_no': '4Ｆ112A-0200X', 'note': ''}
  ],
  'data/BOM\\IF258-S-0385(#13083.2605-0110).xlsx': [
    {'role': 'プレートA ASSY', 'part_no': 'IF258-101ASSY-HR', 'note': ''},
    {'role': 'プレートB', 'part_no': 'IF258/S-702-036', 'note': ''},
    {'role': 'チューブ', 'part_no': 'IF258-104-0385', 'note': ''},
    {'role': '外装箱', 'part_no': '見合った箱', 'note': ''}
  ]
}

parsed_file_path = os.path.join(r"C:\Users\jhatakeyama\.gemini\antigravity\scratch\PartsSearchDB", "parsed_7.json")
with open(parsed_file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Successfully dumped to {parsed_file_path}")
