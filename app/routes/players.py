from flask import jsonify, abort, Blueprint
from flask_pydantic import validate
from flask_jwt_extended import jwt_required, get_jwt_identity

from .. import db
from ..models import User, Player
from ..responses import PostPlayer, UpdatePlayer
from ..schemas import player_schema

cards = Blueprint("cards", __name__, url_prefix = "/api/v1")

#Players
@cards.get('/player')
@jwt_required()
def get_players():
    user_id = get_jwt_identity()
    players = Player.query.all()
    players_schema = []
    
    for player in players:
        schema = player_schema.dump(player)
        schema.update({"own": next((True for user in player.owners if user.id == user_id), False)})
        players_schema.append(schema)
    return {"players": players_schema}, 200

@cards.get('/player/<int:id>')
@jwt_required()
def get_player(id):
    user_id = get_jwt_identity()
    player = Player.query.filter_by(id = id).first()

    if player:
        schema = player_schema.dump(player)
        schema.update({"own": next((True for user in player.owners if user.id == user_id), False)})
        return {"player": schema}, 200

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
    player = Player(name = body['name'], birthdate = body['birthdate'], weight = body['weight'], height = body['height'], role = body["role"])
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
        if body.get('role'):
            player.role = body['role']
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
