import sqlite3

conn = sqlite3.connect("finance.db")

conn.execute("""
    UPDATE deposit
    SET balance = 80000000
""")

conn.commit()
conn.close()

print("Вклад исправлен")