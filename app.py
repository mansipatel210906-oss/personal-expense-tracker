from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "expenses.db"


def create_database():



    connection = sqlite3.connect(DATABASE)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    """)

    connection.commit()
    connection.close()

create_database()


@app.route("/")
def home():

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    expenses = connection.execute("""
        SELECT * FROM expenses
        ORDER BY id DESC
    """).fetchall()

    income = connection.execute("""
        SELECT SUM(amount) AS total
        FROM income
    """).fetchone()["total"]

    expenses_total = connection.execute("""
        SELECT SUM(amount) AS total
        FROM expenses
    """).fetchone()["total"]

    if income is None:
        income = 0

    if expenses_total is None:
        expenses_total = 0

    balance = income - expenses_total

    connection.close()

    return render_template(
        "index.html",
        expenses=expenses,
        income=income,
        expenses_total=expenses_total,
        balance=balance
    )



@app.route("/add", methods=["GET", "POST"])
def add_expense():

    if request.method == "POST":

        title = request.form["title"]
        amount = request.form["amount"]
        category = request.form["category"]
        date = request.form["date"]
        description = request.form["description"]

        connection = sqlite3.connect(DATABASE)

        connection.execute("""
            INSERT INTO expenses
            (title, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
        """, (
            title,
            amount,
            category,
            date,
            description
        ))

        connection.commit()
        connection.close()

        return redirect("/")

    return render_template("add_expense.html")


@app.route("/income", methods=["GET", "POST"])
def add_income():

    if request.method == "POST":

        title = request.form["title"]
        amount = request.form["amount"]
        date = request.form["date"]
        description = request.form["description"]

        connection = sqlite3.connect(DATABASE)

        connection.execute("""
            INSERT INTO income
            (title, amount, date, description)
            VALUES (?, ?, ?, ?)
        """, (
            title,
            amount,
            date,
            description
        ))

        connection.commit()
        connection.close()

        return redirect("/")

    return render_template("income.html")


@app.route("/delete/<int:id>")
def delete_expense(id):

    connection = sqlite3.connect(DATABASE)

    connection.execute(
        "DELETE FROM expenses WHERE id = ?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect("/")



if __name__ == "__main__":
    create_database()
    app.run(host="0.0.0.0", port=5000, debug=False)