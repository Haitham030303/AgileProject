from . import db
from sqlalchemy import func
from flask_login import UserMixin

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    start_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    description = db.Column(db.String(5000), unique=True, nullable=False)
    status = db.Column(db.String(500), nullable=False)

    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(500), nullable=False)
    last_name = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(500), unique=True)
    hash = db.Column(db.String(500))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    task_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    task_description = db.Column(db.String(1000), nullable=False)

class Collaborator(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)

class Leader(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
