from flask import Flask, redirect, render_template
from db import db

app = Flask('name')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budget.db"

db.init_app(app)

from models import User#, Category, Transaction

with app.app_context():
    db.create_all()

@app.route('/')
def home():  
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')
    

if __name__ == "__main__":
    app.run(debug=True)