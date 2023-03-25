from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from views import views

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")
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

def create_databse(app):
    if not path.exists('./' + DB_NAME):
        db.create_all(app=app)


if __name__ == "__main__":
    app.run(debug=True)
