from flask import Blueprint, request, render_template, flash
from flask_login import login_user, login_required, logout_user, current_user
from website.models import Project, User, Leader, Collaborator
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask import redirect, url_for
import re

views = Blueprint("views_bp", __name__)
special_chars = re.compile("[^a-zA-Z0-9 ]")


@views.route("/", methods=["GET"])
@login_required
def index():
    entries = []
    projects = Project.query.all()

    if projects:
        for project in projects:
            entry = {}
            entry["title"] = project.title
            entry["description"] = project.description
            entry["status"] = project.status
            entry["id"] = project.id
            leader_names = []
            collaborator_names = []

            collaborator_entries = Collaborator.query.filter_by(
                project_id=project.id
            ).all()
            leader_entries = Leader.query.filter_by(project_id=project.id).all()

            if leader_entries:
                for leader_entry in leader_entries:
                    leader_first_name = (
                        User.query.filter_by(id=leader_entry.user_id).first().first_name
                    )
                    leader_last_name = (
                        User.query.filter_by(id=leader_entry.user_id).first().last_name
                    )
                    leader_name = leader_first_name + " " + leader_last_name
                    leader_names.append(leader_name)

            if collaborator_entries:
                for collaborator_entry in collaborator_entries:
                    user_id = collaborator_entry.user_id
                    collaborator_first_name = (
                        User.query.filter_by(id=user_id).first().first_name
                    )
                    collaborator_last_name = (
                        User.query.filter_by(id=user_id).first().last_name
                    )
                    collaborator_name = (
                        collaborator_first_name + " " + collaborator_last_name
                    )
                    collaborator_names.append(collaborator_name)
            entry["collaborator_names"] = collaborator_names
            entry["leader_names"] = leader_names
            entries.append(entry)

    return render_template("index.html", entries=entries, user=current_user)


@views.route("/details/<int:id>")
@login_required
def details(id):
    project = Project.query.filter_by(id=id).first()
    collaborators = Collaborator.query.filter_by(project_id=id).all()
    leaders = Leader.query.filter_by(project_id=id).all()
    leader_ids = [
        leader.user_id for leader in leaders
    ]  # Extract the 'user_id' attribute for each Leader object
    collaborator_ids = [collaborator.user_id for collaborator in collaborators]
    users = User.query.filter(User.id.in_(leader_ids)).all()
    collaborator_for_project = User.query.filter(User.id.in_(collaborator_ids)).all()

    if project:
        project_title = project.title
        project_status = project.status
        project_start_date = project.start_date
        project_description = project.description

        if collaborators:
            collaborator_names = ", ".join(
                [
                    user.first_name + " " + user.last_name
                    for user in collaborator_for_project
                ]
            )
        else:
            collaborator_names = ""

        if leaders:
            leader_names = ", ".join(
                [user.first_name + " " + user.last_name for user in users]
            )
        else:
            leader_names = ""

        details = {}
        details["title"] = project_title
        details["status"] = project_status
        details["start_date"] = project_start_date
        details["title"] = project_title
        details["description"] = project_description
        details["collaborator_names"] = collaborator_names
        details["leader_names"] = leader_names

        return render_template("detail.html", user=current_user, details=details)

    return render_template("detail.html", user=current_user)


@views.route("/add_collaborator/<int:id>")
@login_required
def add_collaborator(id):
    collaborators = Collaborator.query.filter_by(project_id=id).all()
    leaders = Leader.query.filter_by(project_id=id).all()
    Already_a_collaborator = False
    Already_a_leader = False
    for collaborator in collaborators:
        if collaborator.user_id == current_user.id:
            Already_a_collaborator = True
            break
    if Already_a_collaborator:
        flash("You are already a collaborator in this project", category="error")
        return redirect(url_for("views_bp.index"))
    for leader in leaders:
        if leader.user_id == current_user.id:
            Already_a_leader = True
            break
    if Already_a_leader:
        flash("You are already a Leader in this project", category="error")
        return redirect(url_for("views_bp.index"))

    new_project = Collaborator(project_id=id, user_id=current_user.id)
    db.session.add(new_project)
    db.session.commit()
    flash("You are now a collaborator in this project.", category="success")
    return redirect(url_for("views_bp.index"))


@views.route("/add_project", methods=["POST", "GET"])
@login_required
def add_project():
    # get project info and store in a txt file for testing
    if request.method == "POST":
        title = request.form.get("title")
        project_leader_emails = request.form.getlist("project_leader[]")
        project_description = request.form.get("project_description")

        project_leader_ids = []
        emails_are_valid = True
        emails = set()
        for email in project_leader_emails:
            leader = User.query.filter_by(email=email).first()
            if not leader:
                emails_are_valid = False
                break
            else:
                project_leader_ids.append(leader.id)
                if email not in emails:
                    emails.add(email)
                else:
                    flash("Please enter each email only once.", category="error")
                    break
        else:
            if len(project_description) < 1:
                flash("project too small", category="error")
            elif len(project_description) > 5000:
                flash("project too large", category="error")
            elif len(title) < 2:
                flash("Title must be at least 2 characters", category="error")
            else:
                # add the project to database
                new_project = Project(title=title, description=project_description)
                db.session.add(new_project)
                db.session.commit()
                for leader_id in project_leader_ids:
                    new_leader = Leader(user_id=leader_id, project_id=new_project.id)
                    db.session.add(new_leader)
                    db.session.commit()
                flash("Project added successfully.", category="success")

        if not emails_are_valid:
            flash(
                "Project Leaders must have an account with the provided email.",
                category="error",
            )

    return render_template("add_project.html", user=current_user)


@views.route("/profile/dashboard")
@login_required
def dashboard():
    user = User.query.filter_by(email=current_user.email).first()
    leaders = Leader.query.filter_by(
        user_id=user.id
    ).all()  # grabbing all the leader's project
    collaborators = Collaborator.query.filter_by(
        user_id=user.id
    ).all()  # grabbing all the leader's project
    entries = []
    collaborator_entries = []
    for leader in leaders:
        projects = Project.query.filter_by(id=leader.project_id).all()
        if projects:
            for project in projects:
                entry = {}
                entry["title"] = project.title
                entry["description"] = project.description
                entry["status"] = project.status
                entry["id"] = project.id
                entry["start_date"] = project.start_date
                entries.append(entry)

    for collaborator in collaborators:
        projects = Project.query.filter_by(id=collaborator.project_id).all()
        if projects:
            for project in projects:
                collaborator_entry = {}
                collaborator_entry["title"] = project.title
                collaborator_entry["description"] = project.description
                collaborator_entry["status"] = project.status
                collaborator_entry["id"] = project.id
                collaborator_entry["start_date"] = project.start_date
                collaborator_entries.append(collaborator_entry)

    
    return render_template(
        "dashboard.html",
        user=current_user,
        entries=entries,
        collaborator_entries=collaborator_entries,
    )


@views.route("/profile/myaccount")
@login_required
def account():
    return render_template("account.html", user=current_user)


@views.route("/profile/change_password", methods=["POST", "GET"])
@login_required
def change_password():
    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password1 = request.form.get("new_password1")
        new_password2 = request.form.get("new_password2")
        if not check_password_hash(current_user.hash, old_password):
            flash("Incorrect password!", category="error")
        elif new_password1 != new_password2:
            flash("New passwords should match!", category="error")
        elif old_password == new_password1:
            flash(
                "New password should be different from current password!",
                category="error",
            )
        elif len(new_password1) < 8:
            flash("Password length must be at least 8 characters!", category="error")
        elif new_password1.islower():  # No uppercase letter
            flash(
                "Password must contain at least one uppercase character!",
                category="error",
            )
        elif new_password1.isupper():  # No lowercase letter
            flash(
                "Password must contain at least one lowercase character",
                category="error",
            )
        elif not special_chars.search(new_password1):
            flash(
                "Password must contain at least one special character!",
                category="error",
            )
        elif not re.search("\d", new_password1):
            flash("Password must contain at least one number!", category="error")
        else:
            current_user.hash = generate_password_hash(new_password1, method="sha256")
            db.session.commit()
            flash("Password changed succesfully", category="success")
            logout_user()
            return redirect("/login")
    return render_template("change_password.html", user=current_user)


@views.route("/profile/edit_profile", methods=["POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        # Check some complexity requirements
        if user and user != current_user:
            flash("A user with this email already exists!", category="error")
        elif first_name and len(first_name) < 2:
            flash("First Name must be at least 2 characters!", category="error")
        elif last_name and len(last_name) < 2:
            flash("Last Name must be at least 2 characters!", category="error")
        elif email and len(email) < 5:
            flash("Email must be at least 5 characters!", category="error")
        else:
            current_user.first_name = first_name or current_user.first_name
            current_user.last_name = last_name or current_user.last_name
            current_user.email = email or current_user.email
            flash("Profile updated successfully!")
            db.session.commit()
    return redirect("/profile/myaccount")
