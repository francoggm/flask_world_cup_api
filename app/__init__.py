from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger

from dotenv import load_dotenv
from uuid import uuid4

import os
import getpass

migrations_path = os.path.dirname(os.path.realpath(__file__))

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

DB_USER = os.environ.get('DATABASE_USER')
DB_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DB_CON = os.environ.get('DATABASE_CON')
DB = os.environ.get('DATABASE')

app = Flask(__name__)
app.config.from_mapping(
    TESTING = True,
    CSRF_ENABLED = True,
    SECRET_KEY = SECRET_KEY,
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_CON}/{DB}",
    SQLALCHEMY_TRACK_MODIFICATIONS = True,
    JWT_SECRET_KEY = JWT_SECRET_KEY
)

db = SQLAlchemy(app)
ma = Marshmallow(app)
swagger = Swagger(app)
migrate = Migrate(app, db, directory = migrations_path + "/migrations")
JWTManager(app)

from .models import User, Team, Player, user_player, player_team
with app.app_context():
    db.create_all()

from .routes.auth import auth
app.register_blueprint(auth)

from .routes.main import routes
app.register_blueprint(routes)

from .routes.players import cards
app.register_blueprint(cards)

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
            username = ''
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

    

