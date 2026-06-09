import sqlite3

conn = sqlite3.connect("finance.db")

for row in conn.execute("SELECT * FROM deposit"):
    print(row)

conn.close()