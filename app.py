"""This is the Main file that runs this program"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from website.auth import auth_bp
from website.views import views_bp
from website.models import db
from website.models import User, Specialty, Profession, Messages
from os import path
from flask_login import LoginManager


# app configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = "This is the secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# registration of blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(views_bp)

# creation of database
if not path.exists('website/database.db'):
    db.create_all(app=app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


if __name__ == "__main__":
    app.run(debug=True)
