from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

import os
import getpass
from uuid import uuid4

app = Flask(__name__)
app.config.from_mapping(
    TESTING = True,
    CSRF_ENABLED = True,
    SECRET_KEY = os.environ.get('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS = True,
    JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
)

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
JWTManager(app)

from .models import User, Team, Player
with app.app_context():
    db.create_all()

from .auth import *
from .users import *
from .routes import *

@app.errorhandler(400)
def generic_error(error):
    return jsonify({"error": error.description}), 400

@app.errorhandler(404)
def item_not_found(error):
    return jsonify({"error": error.description}), 404

@app.cli.command('create-superuser')
def create_superuser():
    username = ''
    while not username:
        username = input('Select a name: ')
        if username == '':
            print('Please enter a valid username')
            continue
        if User.query.filter_by(username = username).first():
            username = None
            print('Username already exists, please select another username!')

    password = getpass.getpass(prompt="Select a password: ")
    if username and password:
        adm = User(username=username, password=password, admin=True, public_id=uuid4())
        db.session.add(adm)
        db.session.commit()

@app.cli.command('reset-superuser')
def create_superuser():
    for user in User.query.filter_by(admin=True):
        if user:
            db.session.delete(user)
    db.session.commit()

    

