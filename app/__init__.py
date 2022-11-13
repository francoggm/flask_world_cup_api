from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

import getpass
from uuid import uuid4

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

from .models import User, Team, Player

with app.app_context():
    db.create_all()

from .auth import *
from .users import *
from .routes import *

@app.cli.command('create-superuser')
def create_superuser():
    username = None
    while not username:
        username = input('Select a name: ')
        if username == '':
            username = None
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

    

