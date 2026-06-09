import sqlite3

conn = sqlite3.connect("finance.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS income (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    income_date DATE NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    comment TEXT
)
""")

conn.commit()
conn.close()

print("База данных создана")