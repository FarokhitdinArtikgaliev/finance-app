import sqlite3

conn = sqlite3.connect("finance.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS mortgage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_debt REAL NOT NULL,
    monthly_payment REAL NOT NULL,
    payment_day INTEGER NOT NULL
)
""")

conn.commit()
conn.close()

print("Таблица ипотеки создана")