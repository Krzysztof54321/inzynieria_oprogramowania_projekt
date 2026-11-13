from flask import Flask, redirect, render_template, request, url_for, session
from db import db
#https://web.budgetbakers.com/pl-PL/dashboard
app = Flask('name')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budget.db"
app.secret_key = "jakis_tymczasowy_sekret"

db.init_app(app)

from models import User, Budget

with app.app_context():
    #db.drop_all()
    db.create_all()


@app.route("/")
def index():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    return render_template(
        "index.html",
        user=user
    )
@app.route('/budget/add', methods=['GET', 'POST'])
def add_budget():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')   # nowe pole
        amount = request.form.get('amount')
        month = request.form.get('month')
        year = request.form.get('year')

        if not all([name, category, amount, month, year]):
            return "Wszystkie pola są wymagane!", 400

        new_budget = Budget(
            name=name,
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

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            print('zalogowano')
            session["user_id"] = user.id
            return redirect(url_for("index"))

        return "Niepoprawny email lub haslo"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        user = User(
            username=username,
            email=email,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        print("utworzony uzytkownik")

        return redirect(url_for("login"))

    return render_template("register.html")
    
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)