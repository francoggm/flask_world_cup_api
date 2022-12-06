from flask import jsonify, make_response, abort, Blueprint
from uuid import uuid4
from flask_pydantic import validate
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from . import db
from .models import User
from .schemas import login_schema, user_schema
from .responses import PostAuth

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

def get_tokens(user, refresh=False):
    access_token = create_access_token(identity = user.id)

    if refresh:
        refresh_token = create_refresh_token(identity = user.id)
        return access_token, refresh_token
    return access_token

@auth.route('/register', methods=['POST'])
@validate()
def register(body: PostAuth):
    username = body.dict().get('username')
    password = body.dict().get('password')

    if len(password) > 4 and len(username) > 1:
        if not User.query.filter_by(username = username).first():
            user = User(username = username, password = password, public_id = uuid4())
            db.session.add(user)
            db.session.commit()
            return make_response(login_schema.dump(user), 201)

        abort(400, description="User already exists")
    abort(400, description="Wrong informations, verify if the username and password (min 5 characters) is valid!")

@auth.route('/login')
@validate()
def login(body: PostAuth):
    username = body.dict().get('username')
    password = body.dict().get('password')

    if username and password:
        user = User.query.filter_by(username = username).first()
        if user:
            if user.check_password(password):
                access_token, refresh_token = get_tokens(user, refresh = True)
                user_response = login_schema.dump(user)
                user_response.update({
                    'access_token': access_token, 
                    'refresh_token': refresh_token
                })
                return make_response(user_response, 200)

            abort(400, description="Wrong password!")
        abort(404, description="User not found!")
    abort(400, description="Wrong credentials!")

@auth.route('/me')
@jwt_required()
def get_self_user():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id = user_id).first()

    if user:
        return make_response(user_schema.dump(user), 200)
    
    abort(404, description="User not found!")

@auth.route('/token/refresh')
@jwt_required(refresh=True)
def refresh_access_token():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id = user_id).first()

    if user:
        access_token = get_tokens(user)
        return jsonify({
            "access_token": access_token
        }), 200
    
    abort(404, description="User not found!")
