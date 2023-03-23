import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    start_date = db.Column(db.DateTime(timezone=True), default=func.now())
    description = db.Column(db.String(5000), unique=True)
    status = db.Column(db.String(500))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(500))
    last_name = db.Column(db.String(500))
    email = db.Column(db.String(500), unique=True)
    hash = db.Column(db.String(500))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    task_date = db.Column(db.DateTime(timezone=True), default=func.now())
    task_description = db.Column(db.String(1000))

class Collaborator(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

class Leader(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
