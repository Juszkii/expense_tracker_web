from flask import Flask, render_template, request, jsonify, redirect
from db import create_table, add_expense, delete_expense, get_expenses, get_by_category

app = Flask(__name__)

create_table()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form["category"]
        description = request.form["description"]
        date = request.form["date"]

        add_expense(amount, category, description, date)

    expenses = get_expenses()
    return render_template("index.html", expenses=expenses)

@app.route("/api/expenses")
def api_expenses():
    expenses = get_expenses()
    return jsonify(expenses)

@app.route("/delete", methods=["POST"])
def delete():
    expense_id = request.form["id"]
    delete_expense(expense_id)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)