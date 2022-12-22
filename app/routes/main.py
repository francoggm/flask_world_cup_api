from flask import jsonify, abort, Blueprint
from flask_pydantic import validate
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from datetime import timedelta, datetime
from uuid import uuid4

from .. import db
from ..models import User, Team, Player
from ..schemas import team_schema, teams_schema, players_schema, player_schema
from ..responses import PostTeam
from ..utils import *

routes = Blueprint("routes", __name__, url_prefix = "/api/v1/user")

#Teams
@routes.get('/team')
@jwt_required()
@swag_from('../docs/teams/get_teams.yml')
def get_teams():
    user_id = get_jwt_identity()
    teams = Team.query.filter_by(user_id = user_id).all()
    return {"teams": teams_schema.dump(teams)}, 200


@routes.get('/team/<string:public_id>')
@jwt_required()
@swag_from('../docs/teams/get_team.yml')
def get_team(public_id):
    user_id = get_jwt_identity()
    team = Team.query.filter_by(user_id = user_id, public_id = public_id).first()
    if team:
        return team_schema.dump(team), 200

    abort(404, description='Team not found!')

@routes.post('/team')
@validate()
@jwt_required()
@swag_from('../docs/teams/create_team.yml')
def create_team(body: PostTeam):
    user_id = get_jwt_identity()
    user = User.query.filter_by(id = user_id).first()
    body = body.dict()
    team = Team(name = body['name'], public_id = uuid4())
    user.teams.append(team)
    db.session.add(team)
    db.session.commit()
    return team_schema.dump(team), 201

@routes.put('/team/<string:public_id>')
@validate()
@jwt_required()
@swag_from('../docs/teams/update_team.yml')
def update_team(public_id, body: PostTeam):
    user_id = get_jwt_identity()
    team = Team.query.filter_by(user_id = user_id, public_id = public_id).first()
    if team:
        body = body.dict()
        team.name = body['name']
        db.session.commit()
        return team_schema.dump(team), 200

    abort(404, description='Team not found!')

@routes.delete('/team/<string:public_id>')
@jwt_required()
@swag_from('../docs/teams/delete_team.yml')
def delete_team(public_id):
    user_id = get_jwt_identity()
    team = Team.query.filter_by(public_id = public_id, user_id = user_id).first()
    if team:
        db.session.delete(team)
        db.session.commit()
        return jsonify({"msg": "Team deleted!"}), 200

    abort(404, description='Team not found!')

@routes.get('/card')
@jwt_required()
@swag_from('../docs/cards/get_cards.yml')
def get_cards():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id = user_id).first()
    return {"cards": players_schema.dump(user.players_owned)}, 200

@routes.delete('/card/<int:id>')
@jwt_required()
@swag_from('../docs/cards/delete_card.yml')
def delete_card(id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(id = user_id).first()
    player = Player.query.filter_by(id = id).first()
    if player:
        if player in user.players_owned:
            user.players_owned.remove(player)
            db.session.commit()
            return jsonify({"msg": "Player deleted from your cards!"}), 200

        abort(400, description = 'Player not found in yours cards!')
    abort(404, description = 'Player not found!')

@routes.put('/team/<string:team_pid>/card/<int:p_id>')
@jwt_required()
@swag_from('../docs/cards/add_team_card.yml')
def add_team_card(team_pid, p_id):
    user_id = get_jwt_identity()
    team = Team.query.filter_by(public_id = team_pid, user_id = user_id).first()
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

@routes.delete('/team/<string:team_pid>/card/<int:p_id>')
@jwt_required()
@swag_from('../docs/cards/delete_team_card.yml')
def delete_team_card(team_pid, p_id):
    user_id = get_jwt_identity()
    team = Team.query.filter_by(public_id = team_pid, user_id = user_id).first()
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
@swag_from('../docs/cards/package.yml')
def user_package():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id = user_id).first()
    if user.last_opening + timedelta(days = 1) < datetime.now():
        user.last_opening = datetime.now()
        players_schema = []
        new_cards = open_package()
        for card in new_cards:
            schema = player_schema.dump(card)
            schema.update({"situation": "Already have!" if card in user.players_owned else "New card!"})
            players_schema.append(schema)
        user.players_owned.extend(new_cards)
        db.session.commit()
        return {"cards": players_schema}, 200

    remains = (user.last_opening + timedelta(days = 1)) - datetime.now()
    remains = timedelta(seconds = remains.seconds)
    return jsonify({"error": f"Still have {str(remains)} hours to open a new package!"}), 408

@routes.get('/teste')
def teste():
    return '<h1>daniel gay</h1>'
    

    



