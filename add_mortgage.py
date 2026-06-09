import sqlite3

conn = sqlite3.connect("finance.db")

conn.execute("DELETE FROM mortgage")

conn.execute("""
INSERT INTO mortgage
(
    total_amount,
    paid_amount,
    remaining_amount,
    current_payment,
    finish_date
)
VALUES
(
    342212200,
    25000000,
    317212200,
    3000000,
    '2031-05-30'
)
""")

conn.commit()
conn.close()

print("Mortgage added")