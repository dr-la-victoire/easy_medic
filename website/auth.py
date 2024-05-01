"""This module contains code for the views part of the app"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.models import db, User, Specialty, Profession, Messages
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not username or not password:
            flash('Username or password cannot be empty', category='error')
        elif user:
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
    if request.method == 'POST':
        category = request.form.get('category')
        if category != 'other':
            return redirect(url_for('auth.doc_reg', category=category))
        else:
            return redirect(url_for('auth.other_reg', category=category))
    return render_template("register.html", user=None)


@auth_bp.route('/doc_reg', strict_slashes=False, methods=['GET', 'POST'])
def doc_reg():
    category = request.args.get('category')
    if request.method == 'POST':
        username = request.form.get('username')
        specialty = request.form.get('specialty')
        password = request.form.get('password')
        password_2 = request.form.get('password_confirm')

        user = User.query.filter_by(username=username).first()

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
            new_user = User(username=username, specialty=Specialty(
                name=specialty), password=generate_password_hash(password, method='sha256'), profession=Profession(name=category))
            db.session.add(new_user)
            db.session.commit()
            flash("You have been successfully registered", category='success')
            return redirect(url_for('auth.login'))

    return render_template("register_doc.html", user=None)


@auth_bp.route('/other_reg', strict_slashes=False, methods=['GET', 'POST'])
def other_reg():
    category = request.args.get('category')
    if request.method == 'POST':
        username = request.form.get('username')
        role = request.form.get('role')
        password = request.form.get('password')
        password_2 = request.form.get('password_confirm')

        user = User.query.filter_by(username=username).first()

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
            new_user = User(username=username, specialty=Specialty(name=role), password=generate_password_hash(
                password, method='sha256'), profession=Profession(name=category))
            db.session.add(new_user)
            db.session.commit()
            flash("You have been successfully registered", category='success')
            return redirect(url_for('auth.login'))

    return render_template('register_other.html', user=None)


@auth_bp.route('/logout', strict_slashes=False)
@login_required
def logout():
    print('Now logging out user')
    logout_user()
    return redirect(url_for('auth.login'))
 