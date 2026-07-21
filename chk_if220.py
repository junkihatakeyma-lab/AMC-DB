import sqlite3
c = sqlite3.connect('部品DB.sqlite')
print(c.execute("SELECT COUNT(*) FROM products WHERE product_code LIKE '%IF220%'").fetchone())
