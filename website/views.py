from flask import Blueprint, request, render_template, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Project



views = Blueprint("views_bp", __name__)

@views.route('/')
@login_required
def index():
    return render_template('index.html', user=current_user)

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
            # TODO: add the project to database 
            db.session.add(new_project)
            new_project = Project(title=title, leaders=project_leader, description=project_description )
            db.session.commit()
            with open('projects.txt', 'a') as f:
                f.write(f'{title} {project_leader} {project_description}\n')
            return "<h1>Project Added!</h1>"
    return render_template('add_project.html', user=current_user)
