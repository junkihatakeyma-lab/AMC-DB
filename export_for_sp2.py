import os
import shutil
from pathlib import Path

source_dir = Path(r"C:\Users\jhatakeyama\.gemini\antigravity\scratch\PartsSearchDB\data")
desktop = Path(r"C:\Users\jhatakeyama\Desktop\SharePointアップロード用")

if not desktop.exists():
    desktop.mkdir(parents=True)

src_path = source_dir / "加工依頼書_自動読取"
dest_path = desktop / "加工依頼書_手書き"

if src_path.exists():
    print(f"Copying {src_path.name} to {dest_path}...")
    shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
    print("Finished copying.")
else:
    print(f"Source folder not found.")
