from flask import Flask, redirect, render_template

app = Flask('name')



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