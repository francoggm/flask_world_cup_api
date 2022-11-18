from flask import jsonify, make_response, abort
from uuid import uuid4
from flask_pydantic import validate

from . import app, db
from .models import User
from .schemas import user_schema, PostAuth

@app.route('/register', methods=['POST'])
@validate()
def register(body: PostAuth):
    username = body.dict().get('username', '')
    password = body.dict().get('password', '')
    if len(password) > 4 and len(username) > 1:
        if not User.query.filter_by(username = username).first():
            user = User(username=username, password=password, public_id=uuid4())
            db.session.add(user)
            db.session.commit()
            return make_response(user_schema.dump(user), 200)
        abort(400, description="User already exists")
    abort(400, description="Wrong informations, verify if the username and password (min 5 characters) is valid!")

@app.route('/login', methods=['POST'])
@validate()
def login(body: PostAuth):
    username = body.dict().get('username', '')
    password = body.dict().get('password', '')
    if username and password:
        user = User.query.filter_by(username = username).first()
        if user:
            if user.check_password(password):
                return make_response(user_schema.dump(user), 200)
            abort(400, description="Wrong password!")
        abort(400, description="User not found!")
    abort(400, description="Wrong credentials!")