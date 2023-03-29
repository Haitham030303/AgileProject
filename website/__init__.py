from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from os import path

DB_NAME = "database.db"
db = SQLAlchemy()

def create_app():
    from website.views import views
    from website.auth import auth

    app = Flask(__name__)
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SECRET_KEY'] = "dsaljf;ldsakjf;lkdsjf,cmlkjlkwqjfoijlsad;"
    db.init_app(app)


    # Ensure templates are auto-reloaded
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    return app


# @app.after_request
# def after_request(response):
#     """Ensure responses aren't cached"""
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     response.headers["Expires"] = 0
#     response.headers["Pragma"] = "no-cache"
#     return response


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()

