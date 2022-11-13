from flask import jsonify, make_response, request
from uuid import uuid4

from . import app, db
from .models import User, user_schema

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if data.get('username') and data.get('password'):
        if not User.query.filter_by(username = data['username']).first():
            user = User(username=data['username'], password=data['password'], public_id=uuid4())
            db.session.add(user)
            db.session.commit()
            return make_response(user_schema.dump(user), 200)
        return make_response(jsonify({"message": "User already exists!"}), 400)
    return make_response(jsonify({"message": "Wrong credentials!"}), 400)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data.get('username') and data.get('password'):
        user = User.query.filter_by(username = data['username']).first()
        if user:
            if user.check_password(data['password']):
                return make_response(user_schema.dump(user), 200)
            return make_response(jsonify({"message": "Wrong password!"}), 401)
        return make_response(jsonify({"message": "User not found!"}), 401)
    return make_response(jsonify({"message": "Wrong credentials!"}), 401)