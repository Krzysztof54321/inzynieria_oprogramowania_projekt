from flask import Flask, redirect, render_template, request, url_for, session
from db import db

app = Flask('name')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budget.db"
app.secret_key = "jakis_tymczasowy_sekret"

db.init_app(app)

from models import User#, Category, Transaction

with app.app_context():
    db.create_all()


@app.route("/")
def home():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    return render_template(
        "index.html",
        user=user
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            print('zalogowano')
            session["user_id"] = user.id
            return redirect(url_for("home"))

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