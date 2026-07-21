import sqlite3
conn=sqlite3.connect('•”•iDB.sqlite')
conn.row_factory=sqlite3.Row
print(conn.execute('SELECT file_path FROM previews WHERE file_path LIKE \'%ŒŸ¸Ø%\' LIMIT 5').fetchall())
