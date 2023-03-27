from flask import Blueprint, render_template, request, flash
import re

auth = Blueprint(__name__, "auth")
special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '{', '}', '[', ']', ';', ':', ',', '<', '>', '.', '?', '/', '|', '\\', '~']

def has_special_char(password):
    for char in password:
        if char in special_chars:
            return True
    return False

@auth.route('/login', methods=["GET", "POST"])
def login():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":       
        return "<h1>Logged In!</h1>"
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')


@auth.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Check some complexity requirements
        if len(first_name) < 2:
            flash('First Name must be at least 2 characters!', category='error')
        elif len(last_name) < 2:
            flash('Last Name must be at least 2 characters!', category='error')
        elif len(email) < 5:
            flash('Email must be at least 5 characters!', category='error')
        elif False:  # TODO: check for existing email
            flash('A user with this email already exists!', category='error')
        elif len(password1) < 8:
            flash('Password length must be at least 8 characters!', category='error')
        elif password1.islower():  # No uppercase letter
            flash('Password must contain at least one uppercase character!', category='error')
        elif password1.isupper():  # No lowercase letter
            flash('Password must contain at least one lowercase character', category='error')
        elif not has_special_char(password1):
            flash('Password must contain at least one special character!', category='error')
        elif not re.search('\d', password1):
            flash('Password must contain at least one number!', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match!', category='error')
        else:
            # TODO: add user to database
            flash('Account created!', category='success')
    return render_template('register.html')
