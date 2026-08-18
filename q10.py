import csv
import glob

# Find the csv file since the name might have encoding issues
csv_files = glob.glob('data/*.csv')
master_csv = [f for f in csv_files if 'マスター' in f or 'マスタ' in f][0]

with open(master_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if '3F136' in row.get('\ufeff25桁品番', '') or '3F136' in row.get('品名', '') or '3F136' in row.get('品名（旧）', ''):
            print(row.get('\ufeff25桁品番') or row.get('25桁品番'), row.get('品名'), row.get('外径'), row.get('高さ'))
