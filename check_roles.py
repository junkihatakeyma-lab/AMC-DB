import sqlite3

conn = sqlite3.connect('部品DB.sqlite')
c = conn.cursor()

c.execute('SELECT DISTINCT role FROM bom_components')
roles = [r[0] for r in c.fetchall() if r[0]]
for role in roles:
    if 'ラベル' in role or '赤字' in role or '特記' in role:
        print(f'Role: "{role}"')

conn.close()
