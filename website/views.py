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
    projects = Project.query.all()
    
    if projects:    
        for project in projects:
            entry = {}
            entry['title'] = project.title
            entry['description'] = project.description
            entry['status'] = project.status
            entry['id'] = project.id
            leader_names = []

            collaborator_entry = Collaborator.query.filter_by(project_id=project.id).first()
            leader_entries = Leader.query.filter_by(project_id=project.id).all()

            if leader_entries:
                for leader_entry in leader_entries:
                    leader_first_name = User.query.filter_by(id=leader_entry.user_id).first().first_name
                    leader_last_name = User.query.filter_by(id=leader_entry.user_id).first().last_name
                    leader_name = leader_first_name + ' ' + leader_last_name
                    leader_names.append(leader_name)

            if collaborator_entry:
                user_id = collaborator_entry.user_id
                user_name = User.query.filter_by(id=user_id).first().name
                entry['user_name'] = user_name
            entry['leader_names'] = leader_names
            entries.append(entry)

    return render_template('index.html', entries=entries, user=current_user)



@views.route('/details/<int:id>')
@login_required
def details(id):
    project = Project.query.filter_by(id=id).first()
    collaborators = Collaborator.query.filter_by(project_id=id).all()
    leaders = Leader.query.filter_by(project_id=id).all()
    leader_ids = [leader.user_id for leader in leaders]  # Extract the 'user_id' attribute for each Leader object
    users = User.query.filter(User.id.in_(leader_ids)).all()

    if project:
        project_title = project.title
        project_status = project.status
        project_start_date = project.start_date
        project_description = project.description

        if collaborators:
            collaborator_names = ', '.join([user.first_name + ' ' + user.last_name for user in users])
        else:
            collaborator_names = ''

        if leaders:
            leader_names = ', '.join([user.first_name + ' ' + user.last_name for user in users])
        else:
            leader_names = ''
         
        details = {}        
        details["title"]=project_title
        details["status"]=project_status
        details["start_date"]=project_start_date
        details["title"]=project_title
        details["description"]=project_description
        details["collaborator_names"]=collaborator_names
        details["leader_names"]=leader_names

        return render_template('detail.html', user=current_user, details=details)

    return render_template('detail.html', user=current_user)





@views.route('/add_project', methods=["POST", "GET"])
@login_required
def add_project():
    # get project info and store in a txt file for testing
    if request.method == 'POST':
        title = request.form.get('title')
        project_leader_emails = request.form.getlist('project_leader[]')
        project_description = request.form.get('project_description')

        project_leader_ids = []
        emails_are_valid=True
        
        for email in project_leader_emails:
            leader = User.query.filter_by(email=email).first()
            if not leader:
                emails_are_valid=False
                break
            else:
                project_leader_ids.append(leader.id)
        else:
            if len(project_description) < 1:
                flash("project too small", category='error')
            elif len(project_description) > 5000:
                flash("project too large", category='error')
            elif len(title) < 2:
                flash("Title must be at least 2 characters", category='error')
            else:
                # add the project to database 
                new_project = Project(title=title, description=project_description)
                db.session.add(new_project)
                db.session.commit()
                for leader_id in project_leader_ids:
                    new_leader = Leader(user_id=leader_id, project_id=new_project.id)
                    db.session.add(new_leader)
                    db.session.commit()
                flash('Project added successfully.', category='success')

        if not emails_are_valid:
            flash("Project Leaders must have an account with the provided email.", category='error')

        
    return render_template('add_project.html', user=current_user)

