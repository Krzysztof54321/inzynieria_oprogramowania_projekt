from flask import Flask, redirect, render_template, request, url_for, session
from db import db
from datetime import datetime
#https://web.budgetbakers.com/pl-PL/dashboard
app = Flask('name')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budget.db"
app.secret_key = "jakis_tymczasowy_sekret"

db.init_app(app)

from models import User, Budget, Transaction

with app.app_context():
    #db.drop_all()
    db.create_all()


@app.route("/")
def index():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    budgets = Budget.query.filter_by(
        user_id=session["user_id"]
    ).all()

    transactions = Transaction.query.filter_by(
        user_id=session["user_id"]
    ).all()

    recent_transactions = Transaction.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Transaction.date.desc()
    ).limit(10).all()

    monthly_income = sum(
        t.amount
        for t in transactions
        if t.type == "income"
    )

    monthly_expense = sum(
        t.amount
        for t in transactions
        if t.type == "expense"
    )

    balance = monthly_income - monthly_expense

    budget_usage = []

    for budget in budgets:

        spent = sum(
            t.amount
            for t in transactions
            if t.type == "expense"
            and t.category == budget.category
            and t.date.month == budget.month
            and t.date.year == budget.year
        )

        percentage = 0

        if budget.amount > 0:
            percentage = min(
                round((spent / float(budget.amount)) * 100),
                100
            )

        budget_usage.append({
            "category": budget.category,
            "month": budget.month,
            "year": budget.year,
            "month_name": budget.month_name,
            "budget": float(budget.amount),
            "spent": spent,
            "percentage": percentage,
            "exceeded": spent > float(budget.amount)
        })
        
    return render_template(
        "index.html",
        user=user,
        monthly_income=monthly_income,
        monthly_expense=monthly_expense,
        balance=balance,
        recent_transactions=recent_transactions,
        budget_usage=budget_usage
    )


@app.route("/budgets")
def budgets():

    if "user_id" not in session:
        return redirect(url_for("login"))

    budgets = Budget.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template(
        "budgets.html",
        budgets=budgets
    )

@app.route('/budget/add', methods=['GET', 'POST'])
def add_budget():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':

        category = request.form.get('category')
        amount = request.form.get('amount')
        month = request.form.get('month')
        year = request.form.get('year')

        if not all([category, amount, month, year]):
            return "Wszystkie pola są wymagane!", 400

        new_budget = Budget(
            user_id=session["user_id"],
            category=category,
            amount=float(amount),
            month=int(month),
            year=int(year)
        )

        try:
            db.session.add(new_budget)
            db.session.commit()

            return redirect(url_for('index'))

        except Exception as e:
            db.session.rollback()
            return f"Błąd zapisu: {e}", 500

    return render_template('budget_form.html')

@app.route('/budget/delete/<int:budget_id>')
def delete_budget(budget_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    budget = Budget.query.get_or_404(
        budget_id
    )

    if budget.user_id != session["user_id"]:
        return "Brak dostępu", 403

    db.session.delete(budget)

    db.session.commit()

    return redirect(
        url_for("budgets")
    )

@app.route('/transaction/add', methods=['GET', 'POST'])
def add_transaction():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':

        transaction = Transaction(
            name=request.form.get("name"),
            amount=float(request.form.get("amount")),
            type=request.form.get("type"),
            category=request.form.get("category"),
            date=datetime.strptime(
                request.form.get("date"),
                "%Y-%m-%d"
            ).date(),
            user_id=session["user_id"]
        )

        db.session.add(transaction)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template(
        "transaction_form.html"
    )

@app.route('/transaction/delete/<int:transaction_id>')
def delete_transaction(transaction_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    transaction = Transaction.query.get_or_404(
        transaction_id
    )

    if transaction.user_id != session["user_id"]:
        return "Brak dostępu", 403

    db.session.delete(transaction)
    db.session.commit()

    return redirect(url_for("transactions"))

@app.route("/transactions")
def transactions():

    if "user_id" not in session:
        return redirect(url_for("login"))

    transactions = Transaction.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Transaction.date.desc()
    ).all()

    return render_template(
        "transactions.html",
        transactions=transactions
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:

            session["user_id"] = user.id

            return redirect(url_for("index"))

        error = "Niepoprawny email lub hasło"

    return render_template(
        "login.html",
        error=error
    )

@app.route("/register", methods=["GET", "POST"])
def register():

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            error = "Konto z takim adresem email już istnieje."

            return render_template(
                "register.html",
                error=error
            )

        existing_username = User.query.filter_by(username=username).first()

        if existing_username:

            error = "Ta nazwa użytkownika jest już zajęta."

            return render_template(
                "register.html",
                error=error
            )
        
        user = User(
            username=username,
            email=email,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template(
        "register.html",
        error=error
    )
    
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)