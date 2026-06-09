import sqlite3

conn = sqlite3.connect("finance.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS mortgage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_amount REAL NOT NULL,
    paid_amount REAL NOT NULL,
    remaining_amount REAL NOT NULL,
    current_payment REAL NOT NULL,
    finish_date TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Mortgage table created")