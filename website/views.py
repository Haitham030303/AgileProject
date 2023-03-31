from flask import Blueprint, request, render_template, flash
from flask_login import login_user, login_required, logout_user, current_user
from website.models import Project, User, Leader, Collaborator
from . import db 
import re

views = Blueprint("views_bp", __name__)
special_chars = re.compile('[^a-zA-Z0-9 ]')


@views.route('/', methods=['GET'])
@login_required
def index():
    entries = []
    descriptions = Project.query.all()
    
    if descriptions:    
        for description in descriptions:
            entry = {}
            entry['title'] = description.title
            entry['description'] = description.description
            entry['status'] = description.status
            entry['id'] = description.id
            collaborator_entry = Collaborator.query.filter_by(project_id=description.id).first()
            leader_entry = Leader.query.filter_by(project_id=description.id).first()
            if leader_entry:
                user_id2 = leader_entry.user_id
                user_name2 = User.query.filter_by(id=user_id2).first().name
                entry['leader_name'] = user_name2
            if collaborator_entry:
                user_id = collaborator_entry.user_id
                user_name = User.query.filter_by(id=user_id).first().name
                entry['user_name'] = user_name
            entries.append(entry)

    return render_template('index.html', entries=entries, user=current_user)



@views.route('/details/<int:id>')
@login_required
def details(id):

    project = Project.query.filter_by(id=id).first()
    collaborators = Collaborator.query.filter_by(project_id=id).all()
    leaders = Leader.query.filter_by(project_id=id).all()

    if project:
         project_title = project.title
         project_status = project.status
         project_start_date = project.start_date
         project_description = project.description

         if collaborators:
             collaborator_names = [c.user.username for c in collaborators]
         else:
             collaborator_names = []

         if leaders:
             leader_names = [l.user.username for l in leaders]
         else:
             leader_names = []

         return render_template('detail.html', user=current_user, project_title=project_title, project_status=project_status, project_start_date=project_start_date, project_description=project_description, collaborator_names=collaborator_names, leader_names=leader_names)

    return render_template('detail.html', user=current_user)




@views.route('/add_project', methods=["POST", "GET"])
@login_required
def add_project():
    # get project info and store in a txt file for testing
    if request.method == 'POST':
        title = request.form.get('title')
        project_leaders = request.form.getlist('project_leaders[]')
        project_description = request.form.get('project_description')
        
        if len(project_description) < 1:
            flash("Description too small", category='error')
        if len(project_description) > 5000:
            flash("Description too large", category='error')
        elif special_chars.search(project_leaders):
            flash('Leader name should not a special character!', category='error')
        elif len(title) < 2:
            flash("Title must be at least 2 characters", category='error')
        # elif len(project_leaders) < 1:
        #     flash("At least two leaders must be added", category='error')
        else:
            # add the project to database 
            new_project = Project(title=title, description=project_description)
            for leader in project_leaders:
                new_project.leaders.append(Leader(name=leader))
            db.session.add(new_project)
            db.session.commit()
            flash('Project added successfully.')
    return render_template('add_project.html', user=current_user)

