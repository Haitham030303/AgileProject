from flask import Blueprint, request, render_template, flash
from flask_login import login_user, login_required, logout_user, current_user
from website.models import Collaborator, Project, User, Leader
from . import db 

views = Blueprint("views_bp", __name__)

@views.route('/', methods=['GET'])
@login_required
def indexs():
    descriptions = Project.query.all()
    entries = []
    for description in descriptions:
        entry = {}
        entry['title'] = description.title
        entry['description'] = description.description
        collaborator_entry = Collaborator.query.filter_by(project_id=description.id).first()
        leader_entry = Leader.query.filter_by(project_id=description.id).first()
        user_id2 = leader_entry.user_id
        user_name2 = User.query.filter_by(id=user_id2).first().name
        user_id = collaborator_entry.user_id
        user_name = User.query.filter_by(id=user_id).first().name
        entry['user_name'] = user_name
        entry['leader_name'] = user_name2
        entries.append(entry)

    return render_template('index.html', entries=entries, user=current_user)

@views.route('/detail')
@login_required
def detail():
    return render_template('detail.html', user=current_user)



@views.route('/add_project', methods=["POST", "GET"])
@login_required
def add_project():
    # get project info and store in a txt file for testing
    if request.method == 'POST':
        title = request.form.get('title')
        project_leaders = request.form.getlist('project_leader[]')
        project_description = request.form.get('project_description')
        
        if len(project_description) < 1:
            flash("description too small", category='error')
        elif len(title) < 2:
            flash("Title must be at least 2 characters", category='error')
        elif len(project_leaders) < 1:
            flash("At least two leaders must be added", category='error')
        else:
            # TODO: add the project to database 
            new_project = Project(title=title, description=project_description )
            for leader in project_leaders:
                new_project.leaders.append(Leader(name=leader))
            db.session.add(new_project)
            db.session.commit()
            return "<h1>Project Added!</h1>"
    return render_template('add_project.html', user=current_user)

