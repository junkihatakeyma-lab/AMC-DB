import os
import shutil
from pathlib import Path

source_dir = Path(r"C:\Users\jhatakeyama\.gemini\antigravity\scratch\PartsSearchDB\data")
desktop = Path(r"C:\Users\jhatakeyama\Desktop\SharePointアップロード用")

folders_to_copy = {
    "図面": "図面",
    "検査証": "検査証",
    "加工依頼書": "加工依頼書",
    "加工依頼書_手書き": "加工依頼書_手書き"
}

if not desktop.exists():
    desktop.mkdir(parents=True)

for src_name, dest_name in folders_to_copy.items():
    src_path = source_dir / src_name
    dest_path = desktop / dest_name
    
    if src_path.exists():
        print(f"Copying {src_name} to {dest_path}...")
        # If destination already exists, we might need to handle it or use shutil.copytree with dirs_exist_ok=True (Python 3.8+)
        shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
        print(f"Finished copying {src_name}.")
    else:
        print(f"Source folder {src_name} not found.")

print("All copies completed successfully!")
