import sqlite3
import os
import glob

def clean_and_run():
    c = sqlite3.connect('部品DB.sqlite')
    c.execute("DELETE FROM previews WHERE file_path LIKE 'data/加工依頼書/%'")
    c.commit()
    print("Deleted old DB entries.")
    
    import generate_previews
    generate_previews.get_all_db_files()
    
    print("Regenerating previews...")
    os.system("python generate_previews.py")

if __name__ == '__main__':
    clean_and_run()
