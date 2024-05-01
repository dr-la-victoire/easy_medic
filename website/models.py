"""This module contains the code for the database models"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func
# from website.models import Messages

db = SQLAlchemy()


class Messages(db.Model):
    """This class forms the model for the messages sent"""
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)

    sender = db.relationship(
        'User', foreign_keys=[sender_id], backref='sent')
    receiver = db.relationship(
        'User', foreign_keys=[receiver_id], backref='received')


class User(db.Model, UserMixin):
    """This class forms the User model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    specialty_id = db.Column(
        db.Integer, db.ForeignKey('specialty.id'), nullable=True)
    profession_id = db.Column(db.Integer, db.ForeignKey(
        'profession.id'), nullable=False)

    profession = db.relationship(
        'Profession', backref=db.backref('users'), lazy=True)
    specialty = db.relationship(
        'Specialty', backref=db.backref('users'), lazy=True)


class Profession(db.Model):
    """This class forms the model of the various professions"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class Specialty(db.Model):
    """This class forms the model of the specialties"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
