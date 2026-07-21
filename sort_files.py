import os
import shutil
import re

INPUT_DIR = r'data\加工依頼書_自動読取'
BOM_DIR = r'data\BOM'
ZUBAN_DIR = r'data\図面'
PHOTO_DIR = r'data\製品写真'

def ensure_dirs():
    for d in [BOM_DIR, ZUBAN_DIR, PHOTO_DIR]:
        os.makedirs(d, exist_ok=True)

def sort_files():
    ensure_dirs()
    if not os.path.exists(INPUT_DIR):
        print(f"Directory {INPUT_DIR} does not exist.")
        return

    files = os.listdir(INPUT_DIR)
    moved_count = 0

    for filename in files:
        file_path = os.path.join(INPUT_DIR, filename)
        if not os.path.isfile(file_path):
            continue
            
        base_name, ext = os.path.splitext(filename)
        
        # 3. 写真 (Photos)
        if "写真" in base_name:
            dest = os.path.join(PHOTO_DIR, filename)
            shutil.move(file_path, dest)
            print(f"Moved {filename} -> 製品写真")
            moved_count += 1
            continue
            
        # Check suffixes for BOM or Drawings
        # Base format is typically #13782 or 稲#13782
        # It could have modifiers like K, A, B, etc.
        # We look at the characters before the extension
        
        if base_name.endswith('K') or base_name.endswith('k'):
            dest = os.path.join(BOM_DIR, filename)
            shutil.move(file_path, dest)
            print(f"Moved {filename} -> BOM")
            moved_count += 1
            continue
            
        # If ends with A, B, C... Z (but not K)
        match = re.search(r'([A-J L-Z a-j l-z])$', base_name)
        if match:
            dest = os.path.join(ZUBAN_DIR, filename)
            shutil.move(file_path, dest)
            print(f"Moved {filename} -> 図面")
            moved_count += 1
            continue

    print(f"\nDone! Moved {moved_count} files.")

if __name__ == "__main__":
    sort_files()
