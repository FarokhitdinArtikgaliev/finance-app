import sqlite3

conn = sqlite3.connect("finance.db")

conn.execute("DELETE FROM deposit")

conn.execute("""
INSERT INTO deposit
(
    balance,
    interest_rate,
    start_date,
    end_date,
    payment_day
)
VALUES
(
    80000000,
    22.52,
    '2026-04-20',
    '2026-10-21',
    21
)
""")

conn.commit()
conn.close()

print("Deposit added")