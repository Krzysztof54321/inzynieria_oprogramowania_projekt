from flask import Flask, redirect, render_template

app = Flask('name')

@app.route('/')
def home():
    return 'hello world'

@app.route('/test')
def test():
    return render_template('index.html')
    

if __name__ == "__main__":
    app.run(debug=True)