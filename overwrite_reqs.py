import sqlite3
import os
import win32com.client
import pythoncom
import fitz

TEMP_DIR = "temp_pdf"
os.makedirs(TEMP_DIR, exist_ok=True)

def overwrite_previews():
    c = sqlite3.connect('部品DB.sqlite', timeout=60)
    # The paths might have backslashes, so use %
    rows = c.execute("SELECT file_path, preview_path FROM previews WHERE file_path LIKE '%加工依頼書%'").fetchall()
    
    if not rows:
        print("No previews found.")
        return
        
    print(f"Found {len(rows)} requests. Starting Excel...")
    pythoncom.CoInitialize()
    excel = win32com.client.DispatchEx("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False
    
    success = 0
    for i, (fp, prev) in enumerate(rows, 1):
        if i % 100 == 0:
            print(f"Restarting Excel at {i}/{len(rows)}")
            excel.Quit()
            import time
            time.sleep(2)
            excel = win32com.client.DispatchEx("Excel.Application")
            excel.Visible = False
            excel.DisplayAlerts = False

        abs_fp = os.path.abspath(fp)
        if not os.path.exists(abs_fp): continue
        
        temp_pdf = os.path.abspath(os.path.join(TEMP_DIR, f"temp_{i}.pdf"))
        
        wb = None
        try:
            wb = excel.Workbooks.Open(abs_fp, UpdateLinks=False, ReadOnly=True)
            for ws in wb.Worksheets:
                try:
                    ws.PageSetup.Zoom = False
                    ws.PageSetup.FitToPagesWide = 1
                    ws.PageSetup.FitToPagesTall = 1
                except:
                    pass
            wb.ExportAsFixedFormat(0, temp_pdf, 0, True, False, 1, 1, False)
        except Exception as e:
            if wb: 
                try: wb.Close(False)
                except: pass
            continue
        finally:
            if wb:
                try: wb.Close(False)
                except: pass
                
        if not os.path.exists(temp_pdf): continue
        
        try:
            doc = fitz.open(temp_pdf)
            page = doc.load_page(0)
            pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
            
            # overwrite the existing preview path
            # The preview path in DB is relative to the backend root or static/
            # For Excel it's usually "previews/xxx.png"
            # In PartsSearchDB, the root is where main.py is.
            out_path = os.path.abspath(prev)
            pix.save(out_path)
            doc.close()
            success += 1
        except Exception as e:
            pass
        finally:
            try: os.remove(temp_pdf)
            except: pass

    excel.Quit()
    print(f"Done! Overwrote {success} previews.")

if __name__ == '__main__':
    overwrite_previews()
