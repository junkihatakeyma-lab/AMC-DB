import sqlite3
conn = sqlite3.connect('部品DB.sqlite')
print("Total rows:", conn.execute("SELECT COUNT(*) FROM simple_files WHERE type='drawing'").fetchone()[0])
print("Distinct paths:", conn.execute("SELECT COUNT(DISTINCT file_path) FROM simple_files WHERE type='drawing'").fetchone()[0])
