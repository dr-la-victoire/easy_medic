"""This module contains code for the views part of the app"""
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from website.models import db, User, Messages, Profession
import json

# creating the blueprint
views_bp = Blueprint('views', __name__)


@views_bp.route('/', strict_slashes=False)
@views_bp.route('/home', strict_slashes=False)
@login_required  # so the user must be logged in to access the home page
def home():
    """This function handles the homepage view"""
    # getting the number of messages the user has not deleted yet
    message_count = Messages.query.filter_by(
        receiver_id=current_user.id).count()
    return render_template("home.html", user=current_user, message_count=message_count)


@views_bp.route('/view_messages', strict_slashes=False)
def view_messages():
    """This function helps the user see all the messages he has"""
    # getting all the messages sent to the user
    message = Messages.query.filter_by(receiver_id=current_user.id).all()
    return render_template("views.html", message=message, user=current_user)


@views_bp.route('/send_messages', strict_slashes=False, methods=['GET', 'POST'])
def send_messages():
    """This function helps the user send messages to other users"""
    # checking if it's a POST request
    # if yes, retrieving the message from the form
    if request.method == 'POST':
        message = request.form.get('message')
        # retrieving the receiver's username
        recipient_username = request.form.get('recipient')

        # checking if the receiver exists
        recipient = User.query.filter_by(username=recipient_username).first()

        if not recipient:
            flash('This username is not registered.', category='error')
        else:
            # sending the message and
            # adding the message to the database if it's the current user sending it
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
    """This function helps the user send a general message"""
    # checking if it's a POST request
    # if yes, retrieving the message from the form
    if request.method == 'POST':
        message = request.form.get('message')
        # getting all the users that belong to a certain profession
        recipients = User.query.join(User.profession).filter(
            Profession.name == profession).all()

        if current_user:
            for person in recipients:
                # adding the message one by one to each of the users selected
                mes = Messages(message=message, receiver=person,
                               sender=current_user)
                db.session.add(mes)
            db.session.commit()
            flash('Your message has been delivered!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Sorry, something went wrong!', category='error')
    return render_template("general.html", user=current_user)


@views_bp.route('/delete', strict_slashes=False, methods=['POST'])
def delete():
    """This function handles the delete message feature"""
    # getting the message id as a JSON object
    message = json.loads(request.data)
    # storing the message id in a variable
    messageId = message['messageId']
    # checking to see whether there's a message with that particular ID
    message = Messages.query.get(messageId)
    if message:  # if there is
        if message.receiver_id == current_user.id:  # and the current user is the one performing the operation
            db.session.delete(message)  # message is deleted
            db.session.commit()  # and the result saved in the database
            flash('Message deleted!', category='success')

    return jsonify({})
