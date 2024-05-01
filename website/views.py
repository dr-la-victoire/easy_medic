"""This module contains code for the views part of the app"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from website.models import db, User, Messages, Profession

views_bp = Blueprint('views', __name__)


@views_bp.route('/', strict_slashes=False)
@views_bp.route('/home', strict_slashes=False)
@login_required
def home():
    message_count = Messages.query.filter_by(
        receiver_id=current_user.id).count()
    return render_template("home.html", user=current_user, message_count=message_count)


@views_bp.route('/view_messages', strict_slashes=False)
def view_messages():
    message = Messages.query.filter_by(receiver_id=current_user.id).all()
    return render_template("views.html", message=message, user=current_user)


@views_bp.route('/send_messages', strict_slashes=False, methods=['GET', 'POST'])
def send_messages():
    if request.method == 'POST':
        message = request.form.get('message')
        recipient_username = request.form.get('recipient')

        recipient = User.query.filter_by(username=recipient_username).first()

        if not recipient:
            flash('This username is not registered.', category='error')
        else:
            if current_user:
                message = Messages(
                    message=message, receiver=recipient, sender=current_user)
                db.session.add(message)
                db.session.commit()
                flash('Your message has been delivered!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Are you sure you are logged in?', category='error')
    return render_template("send.html", user=current_user)


@views_bp.route('/send_general_message/<profession>', strict_slashes=False, methods=['GET', 'POST'])
def send_general_message(profession=None):
    if request.method == 'POST':
        message = request.form.get('message')
        recipients = User.query.join(User.profession).filter(
            Profession.name == profession).all()

        if current_user:
            for person in recipients:
                mes = Messages(message=message, receiver=person,
                               sender=current_user)
                db.session.add(mes)
            db.session.commit()
            flash('Your message has been delivered!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Sorry, something went wrong!', category='error')
    return render_template("general.html", user=current_user)
