"""This module contains code that handles the User Authentication of the web app"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.models import db, User, Specialty, Profession, Messages
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

# setting up the blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    """This function handles the login functionality"""
    # checking if a POST method has been sent
    # if it is, retrieve the username and password with requests
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # filtering to check whether the username exists
        user = User.query.filter_by(username=username).first()

        # logic to login the user
        # if no username or password was passed
        if not username or not password:
            flash('Username or password cannot be empty', category='error')
        elif user:
            # checks if the password is for the username entered
            if check_password_hash(user.password, password):
                flash('You are logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Wrong password', category='error')
        else:
            flash('This username is not registered', category='error')
    return render_template("login.html", user=current_user)


@auth_bp.route('/register', strict_slashes=False, methods=['GET', 'POST'])
def register():
    """This function handles the registration functionality"""
    # checking if a POST method has been sent
    # if it is, retrieving the category from the form
    if request.method == 'POST':
        category = request.form.get('category')
        if category != 'other':
            # redirects to the page for professionals to register
            return redirect(url_for('auth.doc_reg', category=category))
        else:
            # redirects to the general registration page
            return redirect(url_for('auth.other_reg', category=category))
    return render_template("register.html", user=None)


@auth_bp.route('/doc_reg', strict_slashes=False, methods=['GET', 'POST'])
def doc_reg():
    """This function handles the registration for medical professionals"""
    # retrieves the category sent
    category = request.args.get('category')
    # checks if a POST request has been sent
    # if yes, retrieves the required parameters
    if request.method == 'POST':
        username = request.form.get('username')
        specialty = request.form.get('specialty')
        password = request.form.get('password')
        password_2 = request.form.get('password_confirm')

        # checks whether username has been taken
        user = User.query.filter_by(username=username).first()

        # performing necessary registration checks
        if not username:
            flash('Username cannot be empty', category='error')
        elif len(username) < 2:
            flash('Username is too short', category='error')
        elif user:
            flash('Username already exists', category='error')
        elif not specialty:
            flash('Specialty cannot be empty', category='error')
        elif not password or not password_2:
            flash("Password cannot be empty", category='error')
        elif len(password) < 8:
            flash("Password is too short", category='error')
        elif password != password_2:
            flash("Passwords do not match", category='error')
        else:
            # adding the new user to the database
            new_user = User(username=username, specialty=Specialty(
                name=specialty), password=generate_password_hash(password, method='sha256'), profession=Profession(name=category))
            db.session.add(new_user)
            db.session.commit()
            flash("You have been successfully registered", category='success')
            return redirect(url_for('auth.login'))

    return render_template("register_doc.html", user=None)


@auth_bp.route('/other_reg', strict_slashes=False, methods=['GET', 'POST'])
def other_reg():
    """This function handles the registration for the general workers"""
    # retrieves the category sent
    category = request.args.get('category')
    if request.method == 'POST':
        # checks if a POST request has been sent
        # if yes, retrieves the required parameters
        username = request.form.get('username')
        role = request.form.get('role')
        password = request.form.get('password')
        password_2 = request.form.get('password_confirm')

        # checks whether username has been taken
        user = User.query.filter_by(username=username).first()

        # performing necessary registration checks
        if not username:
            flash('Username cannot be empty', category='error')
        elif len(username) < 2:
            flash('Username is too short', category='error')
        elif user:
            flash('Username already exists', category='error')
        elif not role:
            flash('Role cannot be empty', category='error')
        elif not password or not password_2:
            flash("Password cannot be empty", category='error')
        elif len(password) < 8:
            flash("Password is too short", category='error')
        elif password != password_2:
            flash("Passwords do not match", category='error')
        else:
            # adding the new user to the database
            new_user = User(username=username, specialty=Specialty(name=role), password=generate_password_hash(
                password, method='sha256'), profession=Profession(name=category))
            db.session.add(new_user)
            db.session.commit()
            flash("You have been successfully registered", category='success')
            return redirect(url_for('auth.login'))

    return render_template('register_other.html', user=None)


@auth_bp.route('/logout', strict_slashes=False)
@login_required  # this would make sure the user would be logged in before he can logout
def logout():
    """This function handles the logout functionality"""
    logout_user()
    return redirect(url_for('auth.login'))
