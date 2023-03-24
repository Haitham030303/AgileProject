from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
DB_NAME = "database.db"

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SECRET_KEY'] = "dsaljf;ldsakjf;lkdsjf,cmlkjlkwqjfoijlsad;"

db = SQLAlchemy(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

import models

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # TODO: Do validation stuff here
        return "<h1>Logged In!</h1>"
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/add_project')
def add_project():
    return render_template('add_project.html')

def create_databse(app):
    if not path.exists('./' + DB_NAME):
        db.create_all(app=app)


if __name__ == "__main__":
    app.run(debug=True)
