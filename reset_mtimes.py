import sqlite3
c = sqlite3.connect('部品DB.sqlite')
c.execute("DELETE FROM files WHERE file_path LIKE '%.jww'")
c.execute("DELETE FROM files WHERE file_path LIKE '%.wwj'")
c.commit()
