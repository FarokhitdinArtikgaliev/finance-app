import sqlite3

conn = sqlite3.connect("finance.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_date DATE NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    comment TEXT
)
""")

conn.commit()
conn.close()

print("Таблица расходов создана")