from flask import jsonify, abort, Blueprint
from flask_pydantic import validate
from flask_jwt_extended import jwt_required, get_jwt_identity

from . import db
from .models import User, Player
from .responses import PostPlayer, UpdatePlayer
from .schemas import players_schema, player_schema

cards = Blueprint("cards", __name__, url_prefix = "/api/v1/card")

#Players
@cards.get('/player')
def get_players():
    players = Player.query.all()
    if players:
        return players_schema.dump(players), 200
    abort(404, description = 'Players not found!')

@cards.get('/player/<int:id>')
def get_player(id):
    player = Player.query.filter_by(id = id).first()
    if player:
        return player_schema.dump(player), 200
    abort(404, description = 'Player not found!')

@cards.post('/player')
@validate()
@jwt_required()
def create_player(body: PostPlayer):
    user_id = get_jwt_identity()
    user = User.query.filter_by(id = user_id).first()
    if not user.admin:
        return {'error': "You don't have permission!"}, 403

    body = body.dict()
    player = Player(name = body['name'], birthdate = body['birthdate'], weight = body['weight'], height = body['height'])
    db.session.add(player)
    db.session.commit()
    return player_schema.dump(player), 201

@cards.put('/player/<int:id>')
@validate()
@jwt_required()
def update_player(id, body: UpdatePlayer):
    user_id = get_jwt_identity()
    user = User.query.filter_by(id = user_id).first()
    if not user.admin:
        return {'error': "You don't have permission!"}, 403

    player = Player.query.filter_by(id = id).first()
    if player:
        body = body.dict()
        if body.get('name'):
            player.name = body['name']
        if body.get('birthdate'):
            player.birthdate = body['birthdate']
        if body.get('weight'):
            player.weight = body['weight']
        if body.get('height'):
            player.height = body['height']
        db.session.commit()
        return player_schema.dump(player), 200

    abort(404, description='Player not found!')

@cards.delete('/player/<int:id>')
@jwt_required()
def delete_player(id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(id = user_id).first()
    if not user.admin:
        return {'error': "You don't have permission!"}, 403

    player = Player.query.filter_by(id = id).first()
    if player:
        db.session.delete(player)
        db.session.commit()
        return jsonify({"msg": "Player deleted!"}), 200

    abort(404, description='Player not found!')
