import json

output_data = {
    "data/BOM\\4F324-0915(#13554, 2604-0113).xlsx": [
        {"role": "プレートA", "part_no": "IF400D-001", "note": "SECC ｔ1.0, φ324*φ212, （700ｇ）, E-616"},
        {"role": "プレートB", "part_no": "IF400D-002", "note": "SECC ｔ1.0, φ324*φ14, （600ｇ）"},
        {"role": "チューブ", "part_no": "4F324-004-0915", "note": "SECC 5*8, t0.8*911*701L"},
        {"role": "CSナット", "part_no": "4F324-119", "note": "SUS304"},
        {"role": "Ｐ／Ｋ", "part_no": "IF000-007/15-15-R-S", "note": "ネオロン黒, ｔ15*φ283*φ253, 842㎜Ｌにカット, G-17にて繋ぎ・貼り付け"},
        {"role": "外装箱", "part_no": "4F330-0985", "note": "IF400-1000 or IF400-1200, 8.1 kg"},
        {"role": "無地ラベル", "part_no": "無地ラベル", "note": "検査表, or, 荷札"}
    ],
    "data/BOM\\4F455-1700(2段品#13064.13067.13068.13863).xlsx": [
        {"role": "プレートA", "part_no": "4F455-001P", "note": "SECC　ｔ1.0, φ455*φ250, ×3, （1700ｇ）, KB-400 or E-616, 180山時（59㎡）"},
        {"role": "プレートB", "part_no": "4F455-002P", "note": "SECC　ｔ1.0, φ455*φ250/0, ×2"},
        {"role": "チューブ", "part_no": "4F455-004-0850", "note": "SECC　3*4, t0.8*847*817L, ×2"},
        {"role": "外装箱", "part_no": "4F455-1700", "note": "4F455-CP, ×2"},
        {"role": "ラベル", "part_no": "検査表", "note": ""},
        {"role": "荷札", "part_no": "ビニールシート", "note": "（950幅）"},
        {"role": "チャーター", "part_no": "チャーター", "note": "×2, 31.3 kg"}
    ],
    "data/BOM\\4F455-1700(2段品#13859).xlsx": [
        {"role": "プレートA", "part_no": "4F455-001P", "note": "SECC　ｔ1.0, φ455*φ250, ×3, （1600ｇ）, KB-400 or E-616, 235山時（76.7㎡）"},
        {"role": "プレートB", "part_no": "4F455-002P", "note": "SECC　ｔ1.0, φ455*φ250/0, ×2"},
        {"role": "チューブ", "part_no": "4F455-004-0850", "note": "SECC　3*4, t0.8*847*817L"},
        {"role": "外装箱", "part_no": "4F455-1700", "note": "4F455-CP, ×2"},
        {"role": "ラベル", "part_no": "検査表", "note": ""},
        {"role": "荷札", "part_no": "ビニールシート", "note": "（950幅）"},
        {"role": "チャーター", "part_no": "チャーター", "note": "×2, 37 kg"}
    ],
    "data/BOM\\4F455-1700(2段品#13865.13866 BKO PTFE東レ中国).xlsx": [
        {"role": "プレートA", "part_no": "4F455-001P", "note": "SECC　ｔ1.0, φ455*φ250, ×3, （1600ｇ）, KB-400 or E-616, 235山時（76.7㎡）"},
        {"role": "プレートB", "part_no": "4F455-002P", "note": "SECC　ｔ1.0, φ455*φ250/0, ×2"},
        {"role": "チューブ", "part_no": "4F455-004-0850", "note": "SECC　3*4, t0.8*847*817L"},
        {"role": "外装箱", "part_no": "4F455-1700", "note": "4F455-CP, ×2"},
        {"role": "ラベル", "part_no": "検査表", "note": ""},
        {"role": "荷札", "part_no": "ビニールシート", "note": "（950幅）"},
        {"role": "チャーター", "part_no": "チャーター", "note": "×2"}
    ],
    "data/BOM\\4F455-1700(2段品#13867.13868.13869 BKO PTFE東レ中国).xlsx": [
        {"role": "プレートA", "part_no": "4F455-001P", "note": "SECC　ｔ1.0, φ455*φ250, ×3, （1700ｇ）, KB-400 or E-616, 180山時（59㎡）"},
        {"role": "プレートB", "part_no": "4F455-002P", "note": "SECC　ｔ1.0, φ455*φ250/0, ×2"},
        {"role": "チューブ", "part_no": "4F455-004-0850", "note": "SECC　3*4, t0.8*847*817L"},
        {"role": "外装箱", "part_no": "4F455-1700", "note": "4F455-CP, ×2"},
        {"role": "ラベル", "part_no": "検査表", "note": ""},
        {"role": "荷札", "part_no": "ビニールシート", "note": "（950幅）"},
        {"role": "チャーター", "part_no": "チャーター", "note": "×2"}
    ],
    "data/BOM\\5F130改5-0500(#13116 PL対応サンプル ).xlsx": [
        {"role": "プレートA", "part_no": "5F130改5-501", "note": "（1170ｇ）, A:SISAKU-UR-23X-2030A, B:UR-216B"},
        {"role": "プレートB", "part_no": "5F130-502", "note": "（350ｇ）, 吐出NO.27"},
        {"role": "チューブ", "part_no": "IF000-304-0500-80-S", "note": "IF000-304-2000-80-S, トリカルネット支給品, (外径φ80）, H437㎜にカットする"},
        {"role": "外装箱", "part_no": "IF100-0500A（内）", "note": "4F162-0805, 5F130改5-0626, 内1枚カットしてキャップ, （4ヶ入りSカートン・仕切り付）, 内寸法350㎜角×640H"},
        {"role": "メッシュ", "part_no": "5F130-009A", "note": "5Ｆ130-009B, (φ120*φ78), (φ118)"},
        {"role": "ラベル", "part_no": "ラベル", "note": ""},
        {"role": "検査表", "part_no": "検査表", "note": ""},
        {"role": "荷札", "part_no": "荷札", "note": "1.9 kg"}
    ],
    "data/BOM\\5F130改5-0637(#12807).xlsx": [
        {"role": "プレートA", "part_no": "5F130改5-501", "note": "（1170ｇ）, UR-216"},
        {"role": "プレートB", "part_no": "5F130-502", "note": "（350ｇ）, 吐出NO.27"},
        {"role": "チューブ", "part_no": "IF000-304-0500-80-S", "note": "上下でキャップ, トリカルネット支給品, (外径φ80）, H574㎜にする"},
        {"role": "外装箱", "part_no": "IF100-0500A（内）", "note": "4F162-0805, 5F130改5-0787, （4ヶ入りSカートン・仕切り付）"},
        {"role": "マイクロバンド", "part_no": "5F137改用-CLP-SUS", "note": "バインダー IF000-BDG-0030, アース線 SC-90（1050㎜Lにカット）"},
        {"role": "メッシュ", "part_no": "5F130-009A", "note": "5Ｆ130-009B, (φ120*φ78), (φ118)"},
        {"role": "ラベル", "part_no": "ラベル", "note": ""},
        {"role": "検査表", "part_no": "検査表", "note": ""},
        {"role": "荷札", "part_no": "荷札", "note": ""},
        {"role": "ビニール袋", "part_no": "ビニール袋", "note": "2.1 kg"}
    ],
    "data/BOM\\5F130改5-0637(#13876 PL_FS仕様PL MBあり).xlsx": [
        {"role": "プレートA", "part_no": "5F130改5-501", "note": "（1170ｇ）, A:SISAKU-UR-23X-2030A, B:UR-216B"},
        {"role": "プレートB", "part_no": "5F130-502", "note": "（350ｇ）, 吐出NO.27"},
        {"role": "チューブ", "part_no": "IF000-304-0500-80-S", "note": "IF000-304-2000-80-S, トリカルネット支給品, H573㎜にカットする"},
        {"role": "外装箱", "part_no": "IF100-0500A（内）", "note": "4F162-0805, 5F130改5-0626, （4ヶ入りSカートン・仕切り付）, 内寸法350㎜角×640H"},
        {"role": "マイクロバンド", "part_no": "5F137改用-CLP-ALLSUS", "note": "支給品, ※ネジ部SUS304"},
        {"role": "メッシュ", "part_no": "5F130-009A", "note": "5Ｆ130-009B, (φ120*φ78), (φ118)"},
        {"role": "ラベル", "part_no": "ラベル", "note": ""},
        {"role": "検査表", "part_no": "検査表", "note": ""},
        {"role": "荷札", "part_no": "荷札", "note": ""},
        {"role": "ビニール袋", "part_no": "ビニール袋", "note": "2.1 kg"}
    ],
    "data/BOM\\5F130改5-0737(14014.UR-219 C-TF ｱｰｽ線ﾅｼ).xlsx": [
        {"role": "プレートA", "part_no": "5F130改5-501", "note": "UR-219 A : UR-216 B, Ａ100 : Ｂ30"},
        {"role": "プレートB", "part_no": "5F130-502", "note": ""},
        {"role": "チューブ", "part_no": "IF000-304-0500-80-S", "note": "IF000-304-2000-80-S, H674㎜にカットする"},
        {"role": "外装箱", "part_no": "IF100-0500A（内）", "note": "4F162-0805, 5F130改5-0626"},
        {"role": "マイクロバンド", "part_no": "5F137改用-CLP-SUS", "note": ""},
        {"role": "メッシュ", "part_no": "5F130-009A", "note": "5Ｆ130-009Ｂ, (φ120*φ78), (φ118)"},
        {"role": "ラベル", "part_no": "ラベル", "note": ""},
        {"role": "検査表", "part_no": "検査表", "note": ""},
        {"role": "荷札", "part_no": "荷札", "note": ""},
        {"role": "ビニール袋", "part_no": "ビニール袋", "note": ""}
    ],
    "data/BOM\\5F130改5-0737(14051.2605-0048UR-219 C-TF ｱｰｽ線ﾅｼ).xlsx": [
        {"role": "プレートA", "part_no": "5F130改5-501", "note": "UR-219 A : UR-216 B, Ａ100 : Ｂ30"},
        {"role": "プレートB", "part_no": "5F130-502", "note": ""},
        {"role": "チューブ", "part_no": "IF000-304-0500-80-S", "note": "IF000-304-2000-80-S, H674㎜にカットする"},
        {"role": "外装箱", "part_no": "IF100-0500A（内）", "note": "4F162-0805, 5F130改5-0626"},
        {"role": "マイクロバンド", "part_no": "5F137改用-CLP-SUS", "note": ""},
        {"role": "メッシュ", "part_no": "5F130-009A", "note": "5Ｆ130-009Ｂ"},
        {"role": "ラベル", "part_no": "ラベル", "note": ""},
        {"role": "検査表", "part_no": "検査表", "note": ""},
        {"role": "荷札", "part_no": "荷札", "note": ""},
        {"role": "ビニール袋", "part_no": "ビニール袋", "note": ""}
    ],
    "data/BOM\\5F130改5-0787(#12793).xlsx": [
        {"role": "プレートA", "part_no": "5F130改5-501", "note": "UR-216"},
        {"role": "プレートB", "part_no": "5F130-502", "note": ""},
        {"role": "チューブ", "part_no": "IF000-304-0500-80-S", "note": "IF000-304-2000-80-S, H724㎜にカットする"},
        {"role": "外装箱", "part_no": "IF100-0500A（内）", "note": "4F162-0805, 5F130改5-0787"},
        {"role": "マイクロバンド", "part_no": "5F137改用-CLP-ALLSUS", "note": ""},
        {"role": "メッシュ", "part_no": "5F130-009A", "note": "5Ｆ130-009B"},
        {"role": "ラベル", "part_no": "ラベル", "note": ""},
        {"role": "検査表", "part_no": "検査表", "note": ""},
        {"role": "荷札", "part_no": "荷札", "note": ""},
        {"role": "ビニール筒", "part_no": "ビニール筒", "note": ""}
    ],
    "data/BOM\\5F130改5-0937(#13405 UR-219）.xlsx": [
        {"role": "プレートA", "part_no": "5F130改5-501", "note": "UR-219, ※導電仕様の為注意"},
        {"role": "プレートB", "part_no": "5F130-502", "note": ""},
        {"role": "チューブ", "part_no": "IF000-304-2000-80-S", "note": "H874㎜にカット"},
        {"role": "外装箱", "part_no": "IF100-0500A（内）", "note": "5F130改5-1126"},
        {"role": "メッシュ", "part_no": "5F130-009A", "note": "5Ｆ130-009B"},
        {"role": "ビニール袋", "part_no": "ビニール袋", "note": ""},
        {"role": "ラベル", "part_no": "ラベル", "note": ""},
        {"role": "検査表", "part_no": "検査表", "note": ""},
        {"role": "荷札", "part_no": "荷札", "note": ""}
    ],
    "data/BOM\\5F130改5-1137(#12808.マイクロバンド材質違い).xlsx": [
        {"role": "プレートA", "part_no": "5F130改5-501", "note": "UR-216"},
        {"role": "プレートB", "part_no": "5F130-502", "note": ""},
        {"role": "チューブ", "part_no": "IF000-304-2000-80-S", "note": "H1000㎜にカットする×2"},
        {"role": "外装箱", "part_no": "IF100-0500A（内）", "note": "5F130改5-1137"},
        {"role": "マイクロバンド", "part_no": "5F137改用-CLP-SUS", "note": "バインダー IF000-BDG-0030, アース線 SC-90"},
        {"role": "メッシュ", "part_no": "5F130-009A", "note": "5Ｆ130-009B"},
        {"role": "ラベル", "part_no": "ラベル", "note": ""},
        {"role": "検査表", "part_no": "検査表", "note": ""},
        {"role": "荷札", "part_no": "荷札", "note": ""},
        {"role": "ビニール袋", "part_no": "ビニール袋", "note": "2.6 kg"}
    ],
    "data/BOM\\5F130改5-1137(#12901.マイクロバンド材質違い).xlsx": [
        {"role": "プレートA", "part_no": "5F130改5-501", "note": "UR-216"},
        {"role": "プレートB", "part_no": "5F130-502", "note": ""},
        {"role": "チューブ", "part_no": "IF000-304-2000-80-S", "note": "H1000㎜にカットする×2"},
        {"role": "外装箱", "part_no": "IF100-0500A（内）", "note": "5F130改5-1137"},
        {"role": "マイクロバンド", "part_no": "5F137改用-CLP-ALLSUS", "note": "バインダー IF000-BDG-0030, アース線 SC-90"},
        {"role": "メッシュ", "part_no": "5F130-009A", "note": "5Ｆ130-009B"},
        {"role": "ラベル", "part_no": "ラベル", "note": ""},
        {"role": "検査表", "part_no": "検査表", "note": ""},
        {"role": "荷札", "part_no": "荷札", "note": ""},
        {"role": "ビニール袋", "part_no": "ビニール袋", "note": "2.5 kg"}
    ],
    "data/BOM\\5F130改5-1137(#12902.マイクロバンドなし).xlsx": [
        {"role": "プレートA", "part_no": "5F130改5-501", "note": "UR-216"},
        {"role": "プレートB", "part_no": "5F130-502", "note": ""},
        {"role": "チューブ", "part_no": "IF000-304-2000-80-S", "note": "H1000㎜にカットする×2"},
        {"role": "外装箱", "part_no": "IF100-0500A（内）", "note": "5F130改5-1137"},
        {"role": "メッシュ", "part_no": "5F130-009A", "note": "5Ｆ130-009B"},
        {"role": "アース線", "part_no": "SC-90", "note": "バインダー IF000-BDG-0030"},
        {"role": "検査表", "part_no": "検査表", "note": ""},
        {"role": "ラベル", "part_no": "ラベル", "note": ""},
        {"role": "荷札", "part_no": "荷札", "note": ""},
        {"role": "ビニール袋", "part_no": "ビニール袋", "note": "2.5 kg"}
    ],
    "data/BOM\\5F130改5-1137(#13577).xlsx": [
        {"role": "プレートA", "part_no": "5F130改5-501", "note": "UR-216"},
        {"role": "プレートB", "part_no": "5F130-502", "note": ""},
        {"role": "チューブ", "part_no": "IF000-304-2000-80-S", "note": ""},
        {"role": "外装箱", "part_no": "IF100-0500A（内）", "note": "5F130改5-1137"},
        {"role": "メッシュ", "part_no": "5F130-009A", "note": "5Ｆ130-009B"},
        {"role": "ラベル", "part_no": "ラベル", "note": ""},
        {"role": "検査表", "part_no": "検査表", "note": ""},
        {"role": "荷札", "part_no": "荷札", "note": "2.5 kg"}
    ],
    "data/BOM\\5F130改5-1437(#13020 補強バンド数違い).xlsx": [
        {"role": "プレートA", "part_no": "5F130改5-501", "note": "UR-216"},
        {"role": "プレートB", "part_no": "5F130-502", "note": ""},
        {"role": "チューブ", "part_no": "IF000-304-2000-S", "note": "H1374㎜にする"},
        {"role": "外装箱", "part_no": "5F130改5-1437", "note": ""},
        {"role": "メッシュ", "part_no": "5F130-009A", "note": "5Ｆ130-009B"},
        {"role": "ラベル", "part_no": "ラベル", "note": ""},
        {"role": "荷札", "part_no": "荷札", "note": ""},
        {"role": "検査表", "part_no": "検査表", "note": ""}
    ],
    "data/BOM\\5F130改5-1437(#13603.UR-219).xlsx": [
        {"role": "プレートA", "part_no": "5F130改5-501", "note": "UR-219 A : UR-216 B"},
        {"role": "プレートB", "part_no": "5F130-502", "note": ""},
        {"role": "チューブ", "part_no": "IF000-304-2000-80-S", "note": ""},
        {"role": "外装箱", "part_no": "5F130改5-1437", "note": ""},
        {"role": "マイクロバンド", "part_no": "5F137改用-CLP-ALLSUS", "note": ""},
        {"role": "メッシュ", "part_no": "5F130-009A", "note": "5Ｆ130-009Ｂ"},
        {"role": "ラベル", "part_no": "ラベル", "note": ""},
        {"role": "荷札", "part_no": "荷札", "note": ""},
        {"role": "検査表", "part_no": "検査表", "note": ""},
        {"role": "ビニール筒", "part_no": "ビニール筒", "note": ""}
    ],
    "data/BOM\\5F130改5-1637(#13665).xlsx": [
        {"role": "プレートA", "part_no": "5F130改5-501", "note": "UR-216"},
        {"role": "プレートB", "part_no": "5F130-502", "note": ""},
        {"role": "チューブ", "part_no": "IF000-304-2000-80-S", "note": "H1574㎜にする"},
        {"role": "外装箱", "part_no": "5F130改5-2051", "note": "5F130改5-2137, 5F130改5-1637"},
        {"role": "マイクロバンド", "part_no": "5F137改用-CLP-SUS", "note": "バインダー IF000-BDG-0030, アース線 SC-90"},
        {"role": "メッシュ", "part_no": "5F130-009A", "note": "5Ｆ130-009B"},
        {"role": "ラベル", "part_no": "ラベル", "note": ""},
        {"role": "検査表", "part_no": "検査表", "note": ""},
        {"role": "荷札", "part_no": "荷札", "note": ""},
        {"role": "ビニール袋", "part_no": "ビニール袋", "note": "3.0 kg"}
    ],
    "data/BOM\\5F130改5-1637(#13806 MBなし).xlsx": [
        {"role": "プレートA", "part_no": "5F130改5-501", "note": "UR-219 A : UR-216 B"},
        {"role": "プレートB", "part_no": "5F130-502", "note": ""},
        {"role": "チューブ", "part_no": "IF000-304-2000-S", "note": "H1574㎜にする"},
        {"role": "外装箱", "part_no": "5F130改5-1637", "note": "5F130改5-2137"},
        {"role": "メッシュ", "part_no": "5F130-009A", "note": "5Ｆ130-009Ｂ"},
        {"role": "ラベル", "part_no": "ラベル", "note": ""},
        {"role": "検査表", "part_no": "検査表", "note": ""},
        {"role": "荷札", "part_no": "荷札", "note": ""},
        {"role": "ビニール筒", "part_no": "ビニール筒", "note": ""}
    ],
    "data/BOM\\5F130改5-1637(#13981 ﾏｲｸﾛﾊﾞﾝﾄﾞ違い).xlsx": [
        {"role": "プレートA", "part_no": "5F130改5-501", "note": "UR-216"},
        {"role": "プレートB", "part_no": "5F130-502", "note": ""},
        {"role": "チューブ", "part_no": "IF000-304-2000-S", "note": "H1574㎜にする"},
        {"role": "外装箱", "part_no": "5F130改5-1637", "note": "5F130改5-2137"},
        {"role": "マイクロバンド", "part_no": "5F137改用-CLP-ALLSUS", "note": "バインダー IF000-BDG-0030, アース線 IF000-TS/M8"},
        {"role": "メッシュ", "part_no": "5F130-009A", "note": "5Ｆ130-009Ｂ"},
        {"role": "ラベル", "part_no": "ラベル", "note": ""},
        {"role": "検査表", "part_no": "検査表", "note": ""},
        {"role": "荷札", "part_no": "荷札", "note": ""}
    ],
    "data/BOM\\5F130改5-2137(#14057)ﾏｲｸﾛﾊﾞﾝﾄﾞなし.xlsx": [
        {"role": "プレートA", "part_no": "5F130改5-501", "note": "UR-219 A : UR-216 B"},
        {"role": "プレートB", "part_no": "5F130-502", "note": ""},
        {"role": "チューブ", "part_no": "IF000-304-2000-S", "note": "H2074㎜にする"},
        {"role": "外装箱", "part_no": "5F130改5-2137", "note": ""},
        {"role": "メッシュ", "part_no": "5F130-009A", "note": "5Ｆ130-009Ｂ"},
        {"role": "ラベル", "part_no": "ラベル", "note": ""},
        {"role": "検査表", "part_no": "検査表", "note": ""},
        {"role": "荷札", "part_no": "荷札", "note": ""},
        {"role": "ビニール筒", "part_no": "ビニール筒", "note": ""}
    ],
    "data/BOM\\5F132-0556(#13926).xlsx": [
        {"role": "プレートA", "part_no": "5F132-501", "note": "UR-215A.216B"},
        {"role": "プレートB", "part_no": "5F130-502", "note": ""},
        {"role": "チューブ", "part_no": "IF000-304-2000-80-S", "note": "H499㎜にカット"},
        {"role": "外装箱", "part_no": "5F137-0550", "note": ""},
        {"role": "バインダー", "part_no": "IF000-BDG-0030", "note": "アース線"},
        {"role": "メッシュ", "part_no": "5F130-009A", "note": "5Ｆ130-009Ｂ"},
        {"role": "ラベル", "part_no": "ラベル", "note": ""},
        {"role": "荷札", "part_no": "荷札", "note": ""},
        {"role": "検査表", "part_no": "検査表", "note": ""}
    ],
    "data/BOM\\5F132-0655(#12963).xlsx": [
        {"role": "プレートA", "part_no": "5F132-501", "note": "UR-215A.216B"},
        {"role": "プレートB", "part_no": "5F130-502", "note": ""},
        {"role": "チューブ", "part_no": "IF000-304-0500-80-S", "note": "H598㎜にカット"},
        {"role": "バインダー", "part_no": "IF000-BDG-0030", "note": "アース線"},
        {"role": "メッシュ", "part_no": "5F130-009A", "note": "5Ｆ130-009Ｂ"},
        {"role": "外装箱", "part_no": "IF100-0700", "note": "IF100-0500A（内）"},
        {"role": "ビニール袋", "part_no": "ビニール袋", "note": ""},
        {"role": "ラベル", "part_no": "ラベル", "note": ""},
        {"role": "荷札", "part_no": "荷札", "note": ""},
        {"role": "検査表", "part_no": "検査表", "note": ""}
    ]
}

with open('parsed_1.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

print("Saved to parsed_1.json")
