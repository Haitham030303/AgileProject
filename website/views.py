from flask import Blueprint, request, render_template, flash
from flask_login import login_user, login_required, logout_user, current_user
from website.models import Project, User, Leader, Collaborator
from . import db 

views = Blueprint("views_bp", __name__)

@views.route('/', methods=['GET'])
@login_required
def indexs():
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
                user_name2 = User.query.filter_by(id=user_id2).first().first_name
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
    if project:
         project_title = project.title
         project_status = project.status
         project_start_date = project.start_date
         project_description = project.description
         return render_template('detail.html', user=current_user, project_title=project_title, project_status=project_status, project_start_date=project_start_date, project_description=project_description)
   
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
            flash("description too small", category='error')
        elif len(title) < 2:
            flash("Title must be at least 2 characters", category='error')
        # elif len(project_leaders) < 1:
        #     flash("At least two leaders must be added", category='error')
        else:
            # add the project to database 
            new_project = Project(title=title, description=project_description)
            leader_names = request.form.getlist('project_leader[]')
            for name in leader_names:
                full_name = name.split()
                if len(full_name) == 1:
                    first_name = full_name[0]
                    last_name = ''
                else:
                    first_name, last_name = full_name
                leader = User.query.filter_by(first_name=first_name, last_name=last_name).first()
                if not leader:
                    leader = User(first_name=first_name, last_name=last_name)
                new_project.leaders.append(leader)
                db.session.add(leader)
            db.session.add(new_project)
            db.session.commit()
            flash('Project added successfully.')
    return render_template('add_project.html', user=current_user)

