import sqlite3

conn = sqlite3.connect("finance.db")

conn.execute("DROP TABLE IF EXISTS mortgage")

conn.execute("""
CREATE TABLE mortgage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_amount REAL,
    paid_amount REAL,
    remaining_amount REAL,
    current_payment REAL,
    finish_date TEXT
)
""")

conn.commit()
conn.close()

print("Mortgage table recreated")