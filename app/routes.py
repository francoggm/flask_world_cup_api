from flask import make_response, jsonify, abort, Blueprint
from flask_pydantic import validate
from flask_jwt_extended import jwt_required, get_jwt_identity

from . import db
from .models import User, Team, Player
from .schemas import team_schema, teams_schema, player_schema, players_schema
from .schemas_pydantic import PostTeam, PostPlayer, UpdatePlayer

routes = Blueprint("routes", __name__, url_prefix="/api/v1/soccer")

#Teams
@routes.get('/team')
@jwt_required()
def get_teams():
    user_id = get_jwt_identity()
    teams = Team.query.filter_by(user_id = user_id).all()
    if teams:
        return make_response(teams_schema.dump(teams), 200)

    abort(404, description='Teams not found!')

@routes.get('/team/<int:id>')
@jwt_required()
def get_team(id):
    user_id = get_jwt_identity()
    team = Team.query.filter_by(user_id = user_id, id = id).first()
    if team:
        return make_response(team_schema.dump(team), 200)

    abort(404, description='Team not found!')

@routes.post('/team')
@validate()
@jwt_required()
def create_team(body: PostTeam):
    user_id = get_jwt_identity()
    user = User.query.filter_by(id = user_id).first()

    body = body.dict()
    team = Team(name = body['name'])
    user.teams.append(team)

    db.session.add(team)
    db.session.commit()
    return make_response(team_schema.dump(team), 201)

@routes.put('/team/<int:id>')
@validate()
@jwt_required()
def update_team(id, body: PostTeam):
    user_id = get_jwt_identity()
    team = Team.query.filter_by(user_id = user_id, id = id).first()

    if team:
        body = body.dict()
        team.name = body['name']
        db.session.commit()
        return make_response(team_schema.dump(team), 200)

    abort(404, description='Team not found!')

@routes.delete('/team/<int:id>')
@jwt_required()
def delete_team(id):
    user_id = get_jwt_identity()
    team = Team.query.filter_by(id = id, user_id = user_id).first()

    if team:
        db.session.delete(team)
        db.session.commit()
        return make_response(jsonify({"msg": "Team deleted!"}), 200)

    abort(404, description='Team not found!')

@routes.put('/team/<int:t_id>/player/<int:p_id>')
def add_team_player(t_id, p_id):
    team = Team.query.filter_by(id = t_id).first()
    if team:
        player = Player.query.filter_by(id = p_id).first()
        if player:
            if not player in team.players:
                team.players.append(player)
                db.session.commit()
                return make_response(team_schema.dump(team), 200)

            abort(400, description="Player already in this team!")
        abort(404, description='Player not found!')
    abort(404, description='Team not found!')
    

@routes.delete('/team/<int:t_id>/player/<int:p_id>')
def delete_team_player(t_id, p_id):
    team = Team.query.filter_by(id = t_id).first()
    if team:
        player = Player.query.filter_by(id = p_id).first()
        if player:
            if player in team.players:
                team.players.remove(player)
                db.session.commit()
                return make_response(team_schema.dump(team), 200)

            abort(400, description="Player is not in this team!")
        abort(404, description='Player not found!')
    abort(404, description='Team not found!')

#Players
@routes.get('/player')
def get_players():
    players = Player.query.all()
    if players:
        return make_response(players_schema.dump(players), 200)
    abort(404, description='Players not found!')

@routes.get('/player/<int:id>')
def get_player(id):
    player = Player.query.filter_by(id = id).first()
    if player:
        return make_response(player_schema.dump(player), 200)
    abort(404, description='Player not found!')

@routes.post('/player')
@validate()
def create_player(body: PostPlayer):
    body = body.dict()
    player = Player(name = body['name'], birthdate = body['birthdate'], weight = body['weight'], height = body['height'])
    db.session.add(player)
    db.session.commit()
    return make_response(player_schema.dump(player), 201)

@routes.put('/player/<int:id>')
@validate()
def update_player(id, body: UpdatePlayer):
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
        return make_response(player_schema.dump(player), 200)

    abort(404, description='Player not found!')

@routes.delete('/player/<int:id>')
def delete_player(id):
    player = Player.query.filter_by(id = id).first()
    if player:
        db.session.delete(player)
        db.session.commit()
        return make_response(jsonify({"message": "Player deleted!"}), 200)

    abort(404, description='Player not found!')

