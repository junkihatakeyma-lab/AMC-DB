import os
import sys
import sqlite3
import glob
import time
import win32com.client
import fitz  # PyMuPDF
from database import get_db

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = "部品DB.sqlite"
PREVIEWS_DIR = "previews"
TEMP_DIR = "temp_pdf"

def setup_dirs():
    os.makedirs(PREVIEWS_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)

def get_all_db_files():
    conn = get_db()
    c = conn.cursor()
    files = set()
    
    c.execute("SELECT file FROM boms WHERE file IS NOT NULL AND file != ''")
    for row in c.fetchall(): files.add(row[0])
        
    c.execute("SELECT file FROM requests WHERE file IS NOT NULL AND file != ''")
    for row in c.fetchall(): files.add(row[0])
        
    c.execute("SELECT file_path FROM simple_files WHERE file_path IS NOT NULL AND file_path != ''")
    for row in c.fetchall(): files.add(row[0])
        
    conn.close()
    return list(files)

def get_processed_files():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT DISTINCT file_path FROM previews")
    processed = {row[0] for row in c.fetchall()}
    conn.close()
    return processed

def save_preview_to_db(file_path, preview_path, page_num):
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO previews (file_path, page_num, preview_path) VALUES (?, ?, ?)", 
              (file_path, page_num, preview_path))
    conn.commit()
    conn.close()

def convert_excel_to_image(excel_app, file_path, file_id):
    abs_file_path = os.path.abspath(file_path)
    if not os.path.exists(abs_file_path):
        print(f"File not found: {abs_file_path}")
        return False

    temp_pdf = os.path.abspath(os.path.join(TEMP_DIR, f"temp_{file_id}.pdf"))
    
    wb = None
    try:
        wb = excel_app.Workbooks.Open(abs_file_path, UpdateLinks=False, ReadOnly=True)
        
        for ws in wb.Worksheets:
            try:
                ws.PageSetup.Zoom = False
                ws.PageSetup.FitToPagesWide = 1
                ws.PageSetup.FitToPagesTall = 1
            except Exception as e:
                print(f"Warning: Could not set PageSetup for {ws.Name}: {e}")

        # ExportAsFixedFormat: 0 = xlTypePDF
        wb.ExportAsFixedFormat(0, temp_pdf, 0, True, False, 1, 1, False)
    except Exception as e:
        print(f"Error exporting PDF for {file_path}: {e}")
        if wb:
            try: wb.Close(False)
            except: pass
        return False
    finally:
        if wb:
            try: wb.Close(False)
            except: pass

    if not os.path.exists(temp_pdf):
        return False

    # Convert PDF to PNG using PyMuPDF
    try:
        doc = fitz.open(temp_pdf)
        page = doc.load_page(0)  # first page
        # Render at 150 DPI (approx 1.5x zoom)
        pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
        
        # We need a safe filename
        safe_name = os.path.basename(file_path).replace('.xlsx', '').replace('.xls', '')
        preview_filename = f"{safe_name}_{file_id}_p1.png"
        preview_rel_path = os.path.join(PREVIEWS_DIR, preview_filename).replace("\\", "/")
        preview_abs_path = os.path.abspath(preview_rel_path)
        
        pix.save(preview_abs_path)
        doc.close()
        
        save_preview_to_db(file_path, preview_rel_path, 1)
        
        # Cleanup temp pdf
        try: os.remove(temp_pdf)
        except: pass
        
        return True
    except Exception as e:
        print(f"Error rendering PDF to image for {file_path}: {e}")
        return False

def main():
    setup_dirs()
    
    print("Fetching file lists...")
    all_files = get_all_db_files()
    processed = get_processed_files()
    
    pending = [f for f in all_files if f not in processed and f.endswith(('.xlsx', '.xls'))]
    
    total = len(pending)
    print(f"Total files: {len(all_files)}")
    print(f"Already processed: {len(processed)}")
    print(f"Pending to process: {total}")
    
    if total == 0:
        print("All files are already processed!")
        return
        
    print("Starting Excel Application in background...")
    excel = None
    try:
        # Initialize COM
        import pythoncom
        pythoncom.CoInitialize()
        
        os.system("taskkill /F /IM EXCEL.EXE >nul 2>&1")
        excel = win32com.client.DispatchEx("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False
        
        success_count = 0
        for i, file_path in enumerate(pending, 1):
            print(f"[{i}/{total}] Processing {file_path}...")
            # We use `i` just as a unique token for the temp file to avoid collisions
            if convert_excel_to_image(excel, file_path, i):
                success_count += 1
            
            time.sleep(2.0) # Slow down to roughly half the speed to be extra safe on resources
                
            # Restart Excel every 50 files to prevent memory leaks/crashes
            if i % 50 == 0:
                print("Restarting Excel to clear memory...")
                try:
                    excel.Quit()
                except:
                    pass
                del excel
                import gc
                gc.collect()
                os.system("taskkill /F /IM EXCEL.EXE >nul 2>&1")
                time.sleep(2)
                excel = win32com.client.DispatchEx("Excel.Application")
                excel.Visible = False
                excel.DisplayAlerts = False
                
        print(f"\nDone! Successfully created {success_count}/{total} previews.")
        
    except Exception as e:
        print(f"Critical error during Excel operations: {e}")
    finally:
        if excel:
            try:
                excel.Quit()
            except:
                pass
        os.system("taskkill /F /IM EXCEL.EXE >nul 2>&1")
        try:
            import pythoncom
            pythoncom.CoUninitialize()
        except:
            pass

if __name__ == "__main__":
    main()
