from flask import Blueprint, request, render_template

views = Blueprint(__name__, "views")

@views.route('/')
def index():
    return render_template('index.html')


@views.route('/login', methods=["GET", "POST"])
def login():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # TODO: Do validation stuff here
        return "<h1>Logged In!</h1>"
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')


@views.route('/register')
def register():
    return render_template('register.html')


@views.route('/add_project', methods=["POST", "GET"])
def add_project():

    #get project info and store in a txt file for testing
    if request.method == 'POST':
        title = request.form['title']
        project_leader = request.form['project leader']
        project_description = request.form['project description']
        with open('projects.txt', 'a') as f:
            f.write(f'{title}, {project_leader}\n{project_description}\n')
        return "<h1>Project Added!</h1>"
    else:
        return render_template('add_project.html')
