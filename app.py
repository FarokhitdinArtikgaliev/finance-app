from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import date
import sqlite3

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row

    total_income = conn.execute(
        "SELECT IFNULL(SUM(amount), 0) AS total FROM income"
    ).fetchone()["total"]

    total_expense = conn.execute(
        "SELECT IFNULL(SUM(amount), 0) AS total FROM expenses"
    ).fetchone()["total"]

    mortgage_paid = conn.execute("""
        SELECT IFNULL(SUM(amount),0) AS total
        FROM expenses
        WHERE category='Ипотека'
    """).fetchone()["total"]

    balance = total_income - total_expense

    recent_income = conn.execute("""
        SELECT
            income_date as operation_date,
            category,
            amount,
            'income' as operation_type
        FROM income
    """).fetchall()

    recent_expenses = conn.execute("""
        SELECT
            expense_date as operation_date,
            category,
            amount,
            'expense' as operation_type
        FROM expenses
    """).fetchall()

    recent_operations = list(recent_income) + list(recent_expenses)

    recent_operations.sort(
        key=lambda x: x["operation_date"],
        reverse=True
    )

    recent_operations = recent_operations[:10]

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "total_income": total_income,
            "total_expense": total_expense,
            "mortgage_paid": mortgage_paid,
            "balance": balance,
            "recent_operations": recent_operations
        }
    )
# ======================
# ДОХОДЫ
# ======================

@app.get("/income", response_class=HTMLResponse)
def income_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="income.html"
    )


@app.post("/income")
def save_income(
    income_date: str = Form(...),
    amount: float = Form(...),
    category: str = Form(...),
    comment: str = Form("")
):

    conn = sqlite3.connect("finance.db")

    conn.execute(
        """
        INSERT INTO income
        (income_date, amount, category, comment)
        VALUES (?, ?, ?, ?)
        """,
        (income_date, amount, category, comment)
    )

    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/incomes",
        status_code=303
    )


@app.get("/incomes", response_class=HTMLResponse)
def incomes(request: Request):

    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row

    incomes = conn.execute("""
        SELECT *
        FROM income
        ORDER BY income_date DESC, id DESC
    """).fetchall()

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="incomes.html",
        context={
            "incomes": incomes
        }
    )


@app.get("/income/delete/{income_id}")
def delete_income(income_id: int):

    conn = sqlite3.connect("finance.db")

    conn.execute(
        "DELETE FROM income WHERE id = ?",
        (income_id,)
    )

    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/incomes",
        status_code=303
    )


# ======================
# РАСХОДЫ
# ======================

@app.get("/expense", response_class=HTMLResponse)
def expense_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="expense.html"
    )


@app.post("/expense")
def save_expense(
    expense_date: str = Form(...),
    amount: float = Form(...),
    category: str = Form(...),
    comment: str = Form("")
):

    conn = sqlite3.connect("finance.db")

    conn.execute(
        """
        INSERT INTO expenses
        (expense_date, amount, category, comment)
        VALUES (?, ?, ?, ?)
        """,
        (expense_date, amount, category, comment)
    )

    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/expenses",
        status_code=303
    )

    # Пополнение вклада
    if category == "Вклад":

        conn.execute(
            """
            UPDATE deposit
            SET balance = balance + ?
            """,
            (amount,)
        )

    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/expenses",
        status_code=303
    )
@app.get("/expenses", response_class=HTMLResponse)
def expenses(request: Request):

    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row

    expenses = conn.execute("""
        SELECT *
        FROM expenses
        ORDER BY expense_date DESC, id DESC
    """).fetchall()

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="expenses.html",
        context={
            "expenses": expenses
        }
    )


@app.get("/expense/delete/{expense_id}")
def delete_expense(expense_id: int):

    conn = sqlite3.connect("finance.db")

    conn.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/expenses",
        status_code=303
    )
@app.get("/income/edit/{income_id}", response_class=HTMLResponse)
def edit_income_form(income_id: int, request: Request):

    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row

    income = conn.execute(
        "SELECT * FROM income WHERE id = ?",
        (income_id,)
    ).fetchone()

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="edit_income.html",
        context={
            "income": income
        }
    )
@app.post("/income/edit/{income_id}")
def update_income(
    income_id: int,
    income_date: str = Form(...),
    amount: float = Form(...),
    category: str = Form(...),
    comment: str = Form("")
):

    conn = sqlite3.connect("finance.db")

    conn.execute(
        """
        UPDATE income
        SET income_date = ?,
            amount = ?,
            category = ?,
            comment = ?
        WHERE id = ?
        """,
        (income_date, amount, category, comment, income_id)
    )

    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/incomes",
        status_code=303
    )
@app.get("/expense/edit/{expense_id}", response_class=HTMLResponse)
def edit_expense_form(expense_id: int, request: Request):

    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row

    expense = conn.execute(
        "SELECT * FROM expenses WHERE id = ?",
        (expense_id,)
    ).fetchone()

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="edit_expense.html",
        context={
            "expense": expense
        }
    )


@app.post("/expense/edit/{expense_id}")
def update_expense(
    expense_id: int,
    expense_date: str = Form(...),
    amount: float = Form(...),
    category: str = Form(...),
    comment: str = Form("")
):

    conn = sqlite3.connect("finance.db")

    conn.execute(
        """
        UPDATE expenses
        SET expense_date = ?,
            amount = ?,
            category = ?,
            comment = ?
        WHERE id = ?
        """,
        (expense_date, amount, category, comment, expense_id)
    )

    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/expenses",
        status_code=303
    )
@app.get("/mortgage", response_class=HTMLResponse)
def mortgage_page(request: Request):

    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row

    mortgage = conn.execute(
        "SELECT * FROM mortgage LIMIT 1"
    ).fetchone()

    mortgage_expenses = conn.execute("""
        SELECT IFNULL(SUM(amount),0) AS total
        FROM expenses
        WHERE category='Ипотека'
    """).fetchone()["total"]

    total_amount = mortgage["total_amount"]

    current_paid = mortgage["paid_amount"] + mortgage_expenses

    remaining_amount = total_amount - current_paid

    if remaining_amount < 0:
        remaining_amount = 0

    progress = (current_paid / total_amount) * 100

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="mortgage.html",
        context={
            "total_amount": total_amount,
            "current_paid": current_paid,
            "remaining_amount": remaining_amount,
            "current_payment": mortgage["current_payment"],
            "finish_date": mortgage["finish_date"],
            "progress": progress
        }
    )
@app.get("/reports", response_class=HTMLResponse)
def reports(request: Request):

    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row

    expenses = conn.execute("""
        SELECT
            category,
            SUM(amount) total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
    """).fetchall()

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="reports.html",
        context={
            "expenses": expenses
        }
    )
@app.get("/monthly-report", response_class=HTMLResponse)
def monthly_report(request: Request):

    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row

    incomes = conn.execute("""
        SELECT
            substr(income_date,1,7) month,
            SUM(amount) total
        FROM income
        GROUP BY month
        ORDER BY month
    """).fetchall()

    expenses = conn.execute("""
        SELECT
            substr(expense_date,1,7) month,
            SUM(amount) total
        FROM expenses
        GROUP BY month
        ORDER BY month
    """).fetchall()

    conn.close()

    income_labels = [row["month"] for row in incomes]
    income_values = [row["total"] for row in incomes]

    expense_values = []

    expense_dict = {
        row["month"]: row["total"]
        for row in expenses
    }

    for month in income_labels:
        expense_values.append(
            expense_dict.get(month, 0)
        )

    return templates.TemplateResponse(
        request=request,
        name="monthly_report.html",
        context={
            "incomes": incomes,
            "expenses": expenses,
            "labels": income_labels,
            "income_values": income_values,
            "expense_values": expense_values
        }
    )
@app.get("/deposit", response_class=HTMLResponse)
def deposit_page(request: Request):

    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row

    deposit = conn.execute(
        "SELECT * FROM deposit LIMIT 1"
    ).fetchone()

    total_topups = conn.execute("""
        SELECT IFNULL(SUM(amount),0) AS total
        FROM expenses
        WHERE category='Вклад'
    """).fetchone()["total"]
    topups = conn.execute("""
    SELECT
        expense_date,
        amount,
        comment
    FROM expenses
    WHERE category='Вклад'
    ORDER BY expense_date DESC, id DESC
""").fetchall()

    start_balance = deposit["balance"]

    current_balance = start_balance + total_topups

    rate = deposit["interest_rate"]

    monthly_income = current_balance * rate / 100 / 12
    yearly_income = current_balance * rate / 100

    today = date.today()

    current_year = today.year
    current_month = today.month

    payment_day = deposit["payment_day"]

    try:

        next_payment = date(
            current_year,
            current_month,
            payment_day
        )

        if next_payment <= today:

            if current_month == 12:
                next_payment = date(
                    current_year + 1,
                    1,
                    payment_day
                )
            else:
                next_payment = date(
                    current_year,
                    current_month + 1,
                    payment_day
                )

    except:
        next_payment = today

    days_left = (next_payment - today).days

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="deposit.html",
        context={
            "balance": current_balance,
            "topups": topups,
            "rate": rate,
            "monthly_income": monthly_income,
            "yearly_income": yearly_income,
            "start_date": deposit["start_date"],
            "end_date": deposit["end_date"],
            "payment_day": deposit["payment_day"],
            "days_left": days_left,
            "total_topups": total_topups
        }
    )
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row

    income_data = conn.execute("""
        SELECT
            substr(income_date,1,7) month,
            SUM(amount) total
        FROM income
        GROUP BY month
        ORDER BY month
    """).fetchall()

    expense_data = conn.execute("""
        SELECT
            substr(expense_date,1,7) month,
            SUM(amount) total
        FROM expenses
        GROUP BY month
        ORDER BY month
    """).fetchall()

    expense_categories = conn.execute("""
        SELECT
            category,
            SUM(amount) total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
    """).fetchall()

    conn.close()

    months = [row["month"] for row in income_data]
    incomes = [row["total"] for row in income_data]

    expense_dict = {
        row["month"]: row["total"]
        for row in expense_data
    }

    expenses = [
        expense_dict.get(month, 0)
        for month in months
    ]

    category_labels = [
        row["category"]
        for row in expense_categories
    ]

    category_values = [
        row["total"]
        for row in expense_categories
    ]

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "months": months,
            "incomes": incomes,
            "expenses": expenses,
            "category_labels": category_labels,
            "category_values": category_values
        }
    )