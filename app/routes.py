from flask import jsonify, abort, Blueprint
from flask_pydantic import validate
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import timedelta, datetime
import random

from . import db
from .models import User, Team, Player
from .schemas import team_schema, teams_schema, players_schema, player_schema
from .responses import PostTeam

routes = Blueprint("routes", __name__, url_prefix = "/api/v1/user")

def player_have_team(player, user_teams):
    for team in user_teams:
        if player in team.players_owned:
            return True
    return False

def open_package(cards_count = 2):
    players = Player.query.all()
    new_cards = [random.choice(players) for _ in cards_count]
    return new_cards

#Teams
@routes.get('/team')
@jwt_required()
def get_teams():
    user_id = get_jwt_identity()
    teams = Team.query.filter_by(user_id = user_id).all()
    if teams:
        return teams_schema.dump(teams), 200

    abort(404, description='Teams not found!')

@routes.get('/team/<int:id>')
@jwt_required()
def get_team(id):
    user_id = get_jwt_identity()
    team = Team.query.filter_by(user_id = user_id, id = id).first()
    if team:
        return team_schema.dump(team), 200

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
    return team_schema.dump(team), 201

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
        return team_schema.dump(team), 200

    abort(404, description='Team not found!')

@routes.delete('/team/<int:id>')
@jwt_required()
def delete_team(id):
    user_id = get_jwt_identity()
    team = Team.query.filter_by(id = id, user_id = user_id).first()

    if team:
        db.session.delete(team)
        db.session.commit()
        return jsonify({"msg": "Team deleted!"}), 200

    abort(404, description='Team not found!')

@routes.get('/player')
@jwt_required()
def get_players():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id = user_id).first()

    return players_schema.dump(user.players_owned), 200

@routes.delete('/player/<int:id>')
@jwt_required()
def delete_players(id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(id = user_id).first()
    player = Player.query.filter_by(id = id).first()
    if player:
        if player in user.players_owned:
            user.players_owned.remove(player)
            db.session.commit()
            return jsonify({"msg": "Player deleted from your cards!"}), 200

        abort(404, description='Player not found in yours cards!')
    abort(404, description='Player not found!')

@routes.put('/team/<int:t_id>/player/<int:p_id>')
@jwt_required()
def add_team_player(t_id, p_id):
    user_id = get_jwt_identity()
    team = Team.query.filter_by(id = t_id, user_id = user_id).first()
    user = User.query.filter_by(id = user_id).first()

    if team:
        player = Player.query.filter_by(id = p_id).first()
        if player:
            if player in user.players_owned:
                if not player_have_team(player, user.teams):
                    team.players_owned.append(player)
                    db.session.commit()
                    return team_schema.dump(team), 200

                abort(400, description='Player is already in one of your teams!')
            abort(404, description='Player not found in your cards!')
        abort(404, description='Player not found!')
    abort(404, description='Team not found!')

@routes.delete('/team/<int:t_id>/player/<int:p_id>')
@jwt_required()
def delete_team_player(t_id, p_id):
    user_id = get_jwt_identity()
    team = Team.query.filter_by(id = t_id, user_id = user_id).first()

    if team:
        user = User.query.filter_by(id = user_id).first()
        player = Player.query.filter_by(id = p_id).first()
        if player:
            if player in user.players_owned:
                if player in team.players_owned:
                    team.players_owned.remove(player)
                    db.session.commit()
                    return team_schema.dump(team), 200

                abort(400, description='Player not in this team!')
            abort(404, description='Player not found in your cards!')
        abort(404, description='Player not found!')
    abort(404, description='Team not found!')

@routes.get('/package')
@jwt_required()
def open_package():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id = user_id).first()
    
    if user.last_opening + timedelta(days = 1) < datetime.now():
        user.last_opening = datetime.now()
        # players_schema = []
        # new_cards = open_package()
        # for card in new_cards:
        #     schema = player_schema(card)
        #     schema.update({"situation": "Already have!" if card in user.players_owned else "New card!"})
        #     players_schema.append(schema)
        # user.players_owned.extend(new_cards)
        db.session.commit()
        # return players_schema, 200
        return {}

    remains = (user.last_opening + timedelta(days = 1)) - datetime.now()
    remains = timedelta(seconds = remains.seconds)
    return jsonify({"error": f"Still have {str(remains)} hours to open a new package!"}), 408
    

    



