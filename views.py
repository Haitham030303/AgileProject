from flask import Blueprint, request, render_template

views = Blueprint(__name__, "views")

@views.route('/')
def index():
    return render_template('index.html')


@views.route('/add_project', methods=["POST", "GET"])
def add_project():

    # get project info and store in a txt file for testing
    if request.method == 'POST':
        title = request.form['title']
        project_leader = request.form['project leader']
        project_description = request.form['project description']
        with open('projects.txt', 'a') as f:
            f.write(f'{title}, {project_leader}\n{project_description}\n')
        return "<h1>Project Added!</h1>"
    else:
        return render_template('add_project.html')
