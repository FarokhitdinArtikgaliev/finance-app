import sqlite3

conn = sqlite3.connect("finance.db")
conn.row_factory = sqlite3.Row

result = conn.execute("""
    SELECT IFNULL(SUM(amount),0) total
    FROM expenses
    WHERE category='Вклад'
""").fetchone()

print("Пополнения:", result["total"])

conn.close()