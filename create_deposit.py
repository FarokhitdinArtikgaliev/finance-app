import sqlite3

conn = sqlite3.connect("finance.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS deposit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    balance REAL,
    interest_rate REAL,
    start_date TEXT,
    end_date TEXT,
    payment_day INTEGER
)
""")

conn.commit()
conn.close()

print("Deposit table created")