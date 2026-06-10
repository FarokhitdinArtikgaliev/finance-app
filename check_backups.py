import sqlite3

files = [
    "backups/finance_20260609_1555.db",
    "backups/finance_20260609_1559.db",
    "backups/finance_20260609_1600.db"
]

for db in files:
    conn = sqlite3.connect(db)
    expenses = conn.execute(
        "SELECT COUNT(*) FROM expenses"
    ).fetchone()[0]

    print(db, "expenses =", expenses)

    conn.close()