import sqlite3

conn = sqlite3.connect('部品DB.sqlite')
conn.execute("DELETE FROM files WHERE file_path LIKE 'data/BOM/%'")
conn.execute('DELETE FROM boms')
conn.execute('DELETE FROM bom_components')
conn.execute('DELETE FROM bom_requests')
conn.commit()
conn.close()
print("Cleared BOM cache from DB")
