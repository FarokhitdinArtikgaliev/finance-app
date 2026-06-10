import sqlite3

from database import get_connection

# SQLite
sqlite_conn = sqlite3.connect("finance.db")
sqlite_conn.row_factory = sqlite3.Row

# PostgreSQL
pg_conn = get_connection()
pg_cur = pg_conn.cursor()

# ------------------
# income
# ------------------

rows = sqlite_conn.execute(
    "SELECT * FROM income"
).fetchall()

for row in rows:
    pg_cur.execute("""
        INSERT INTO income
        (income_date, amount, category, comment)
        VALUES (%s, %s, %s, %s)
    """, (
        row["income_date"],
        row["amount"],
        row["category"],
        row["comment"]
    ))

print("Income:", len(rows))

# ------------------
# expenses
# ------------------

rows = sqlite_conn.execute(
    "SELECT * FROM expenses"
).fetchall()

for row in rows:
    pg_cur.execute("""
        INSERT INTO expenses
        (expense_date, amount, category, comment)
        VALUES (%s, %s, %s, %s)
    """, (
        row["expense_date"],
        row["amount"],
        row["category"],
        row["comment"]
    ))

print("Expenses:", len(rows))

# ------------------
# mortgage
# ------------------

rows = sqlite_conn.execute(
    "SELECT * FROM mortgage"
).fetchall()

for row in rows:
    pg_cur.execute("""
        INSERT INTO mortgage
        (
            total_amount,
            paid_amount,
            remaining_amount,
            current_payment,
            finish_date
        )
        VALUES (%s,%s,%s,%s,%s)
    """, (
        row["total_amount"],
        row["paid_amount"],
        row["remaining_amount"],
        row["current_payment"],
        row["finish_date"]
    ))

print("Mortgage:", len(rows))

# ------------------
# deposit
# ------------------

rows = sqlite_conn.execute(
    "SELECT * FROM deposit"
).fetchall()

for row in rows:
    pg_cur.execute("""
        INSERT INTO deposit
        (
            balance,
            interest_rate,
            start_date,
            end_date,
            payment_day
        )
        VALUES (%s,%s,%s,%s,%s)
    """, (
        row["balance"],
        row["interest_rate"],
        row["start_date"],
        row["end_date"],
        row["payment_day"]
    ))

print("Deposit:", len(rows))

pg_conn.commit()

sqlite_conn.close()
pg_conn.close()

print("MIGRATION COMPLETED")