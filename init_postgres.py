from database import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS income (
    id SERIAL PRIMARY KEY,
    income_date TEXT,
    amount DOUBLE PRECISION,
    category TEXT,
    comment TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id SERIAL PRIMARY KEY,
    expense_date TEXT,
    amount DOUBLE PRECISION,
    category TEXT,
    comment TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS mortgage (
    id SERIAL PRIMARY KEY,
    total_amount DOUBLE PRECISION,
    paid_amount DOUBLE PRECISION,
    remaining_amount DOUBLE PRECISION,
    current_payment DOUBLE PRECISION,
    finish_date TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS deposit (
    id SERIAL PRIMARY KEY,
    balance DOUBLE PRECISION,
    interest_rate DOUBLE PRECISION,
    start_date TEXT,
    end_date TEXT,
    payment_day INTEGER
)
""")

conn.commit()
conn.close()

print("POSTGRES TABLES CREATED")