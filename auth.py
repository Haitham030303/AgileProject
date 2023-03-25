from flask import Blueprint, render_template, request

auth = Blueprint(__name__, "auth")

@auth.route('/login', methods=["GET", "POST"])
def login():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # TODO: Do validation stuff here
        return "<h1>Logged In!</h1>"
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')


@auth.route('/register')
def register():
    return render_template('register.html')
