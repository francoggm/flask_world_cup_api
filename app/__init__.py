from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import getpass

def create_db():
    db_name = 'sqlite:///worldcup.db'.split('/')[-1]
    if not db_name in os.listdir(os.getcwd()):
        db.create_all()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///worldcup.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'random_string'

db = SQLAlchemy(app)

from .models import Team, Player
create_db()

@app.cli.command('create-superuser')
def create_superuser():
    name = input('Select a name: ')
    password = getpass.getpass(prompt="Select a password: ")