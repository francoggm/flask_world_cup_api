from flask import make_response, jsonify, abort, Blueprint
from flask_pydantic import validate
from flask_jwt_extended import jwt_required, get_jwt_identity

from . import db
from .models import User, Team, Player, UserCollection
from .schemas import team_schema, teams_schema, players_schema
from .schemas_pydantic import PostTeam

routes = Blueprint("routes", __name__, url_prefix="/api/v1/user")

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
@jwt_required()
def add_team_player(t_id, p_id):
    user_id = get_jwt_identity()
    team = Team.query.filter_by(id = t_id, user_id = user_id).first()

    if team:
        collection = UserCollection.query.filter_by(user_id = user_id, player_id = p_id, team_id = None).first()
        if collection:
            for player in team.players:
                if p_id == player.player_id:
                    abort(400, description='Player already in this team!')
            team.players.append(collection)
            db.session.commit()
            return make_response(team_schema.dump(team), 200)

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

@routes.get('/cards')
@jwt_required()
def get_players():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id = user_id).first()
    players = Player.query.filter(Player.id.in_([collection.player_id for collection in user.collections]))
    return players_schema.dump(players), 200

