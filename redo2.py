import sqlite3
import os

def clean_and_run():
    c = sqlite3.connect('部品DB.sqlite', timeout=60)
    c.execute("DELETE FROM previews WHERE file_path LIKE 'data/加工依頼書/%'")
    c.commit()
    print("Deleted old DB entries.")
    
    import generate_previews
    pending = []
    import glob
    for fp in glob.glob("data/加工依頼書/*.xlsx"):
        pending.append(fp)
        
    print(f"Regenerating previews for {len(pending)} files...")
    excel = None
    import win32com.client
    import pythoncom
    pythoncom.CoInitialize()
    excel = win32com.client.DispatchEx("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False
    
    for i, fp in enumerate(pending, 1):
        generate_previews.convert_excel_to_image(excel, fp, f"req_{i}")
        
    excel.Quit()
    print("Done!")

if __name__ == '__main__':
    clean_and_run()
