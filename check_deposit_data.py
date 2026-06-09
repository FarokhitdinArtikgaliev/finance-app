import sqlite3

conn = sqlite3.connect("finance.db")
conn.row_factory = sqlite3.Row

deposit = conn.execute(
    "SELECT * FROM deposit LIMIT 1"
).fetchone()

print(dict(deposit))

conn.close()