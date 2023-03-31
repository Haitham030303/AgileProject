from flask import Blueprint, request, render_template, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from .models import Project, User
from . import db 

views = Blueprint("views_bp", __name__)

@app.route('/', methods=['GET'])
@login_required
def indexs():
    descriptions = Project.query.all()
    entries = []
    for description in descriptions:
        entry = {}
        entry['title'] = description.title
        entry['description'] = description.description
        collaborator_entry = collaborator.query.filter_by(project_id=description.id).first()
        user_id = collaborator_entry.user_id
        user_name = User.query.filter_by(id=user_id).first().name
        entry['user_name'] = user_name
        entries.append(entry)

    return render_template('index.html', entries=entries)

@views.route('/detail')
@login_required
def detail():
    return render_template('detail.html', user=current_user)


@views.route('/add_project', methods=["POST", "GET"])
@login_required
def add_project():
    # get project info and store in a txt file for testing
    if request.method == 'POST':
        title = request.form['title']
        project_leader = request.form['project_leader']
        project_description = request.form['project_description']
        
        if len(project_description) < 1:
            flash("description too small", category='error')
        elif len(title) < 2:
            flash("Title must be at least 2 characters", category='error')
        elif len(project_leader) < 2:
            flash("Name must be at least 2 characters", category='error')
        else:
            new_project = Project(title=title, leaders=project_leader, description=project_description)
            db.session.add(new_project)
            db.session.commit()
            return "<h1>Project Added!</h1>"
    return render_template('add_project.html', user=current_user)
