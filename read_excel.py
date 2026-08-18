import pandas as pd
import json

df = pd.read_excel('data/部品マスタ/部品マスタ.xlsx')
result = {
    "columns": list(df.columns),
    "sample": df.head(5).to_dict(orient='records')
}

with open('temp_master.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
