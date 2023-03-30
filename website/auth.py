from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
import re
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)
special_chars = re.compile('[^a-zA-Z0-9 ]')


@auth.route('/login', methods=["GET", "POST"])
def login():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.hash, password):
                flash('Logged in successfully!', category='success')
                return redirect('/')
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    # User reached route via GET (as by clicking a link or via redirect)
    return render_template('login.html', boolean=True)


@auth.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        # Check some complexity requirements
        if user:
            flash('A user with this email already exists!', category='error')
        elif len(first_name) < 2:
            flash('First Name must be at least 2 characters!', category='error')
        elif len(last_name) < 2:
            flash('Last Name must be at least 2 characters!', category='error')
        elif len(email) < 5:
            flash('Email must be at least 5 characters!', category='error')
        elif len(password1) < 8:
            flash('Password length must be at least 8 characters!', category='error')
        elif password1.islower():  # No uppercase letter
            flash('Password must contain at least one uppercase character!', category='error')
        elif password1.isupper():  # No lowercase letter
            flash('Password must contain at least one lowercase character', category='error')
        elif not special_chars.search(password1):
            flash('Password must contain at least one special character!', category='error')
        elif not re.search('\d', password1):
            flash('Password must contain at least one number!', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match!', category='error')
        else:
            new_user = User(email=email, first_name=first_name, 
                            last_name=last_name, hash=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect('/')
    return render_template('register.html')

@auth.route('/logout')
def logout():
