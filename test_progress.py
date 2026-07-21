import sqlite3

conn = sqlite3.connect('部品DB.sqlite')
c = conn.cursor()

c.execute('SELECT COUNT(DISTINCT file_path) FROM previews')
done = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM simple_files WHERE type IN ('inspection', 'drawing', 'photo')")
total = c.fetchone()[0]

c.execute('SELECT COUNT(*) FROM boms')
total += c.fetchone()[0]

c.execute('SELECT COUNT(*) FROM requests')
total += c.fetchone()[0]

print(f'Done: {done} / Total: {total}')
