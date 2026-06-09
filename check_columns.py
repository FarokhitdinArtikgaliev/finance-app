import sqlite3

conn = sqlite3.connect("finance.db")

rows = conn.execute("""
PRAGMA table_info(mortgage)
""").fetchall()

for row in rows:
    print(row)

conn.close()