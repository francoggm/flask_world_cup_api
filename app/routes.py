from flask import make_response, jsonify, abort, Blueprint
from flask_pydantic import validate

from . import app, db
from .models import User, Team, Player, Coach
from .schemas import team_schema, teams_schema, player_schema, players_schema, coach_schema, coachs_schema
from .schemas_pydantic import PostTeam, PostPlayer, PostCoach, UpdatePlayer, UpdateCoach, UpdateTeam

routes = Blueprint("routes", __name__, url_prefix="/api/v1/soccer")

#Teams
@routes.get('/team')
def get_teams():
    teams = Team.query.all()
    if teams:
        return make_response(teams_schema.dump(teams), 200)

    abort(404, description='Teams not found!')

@routes.get('/team/<int:id>')
def get_team(id):
    team = Team.query.filter_by(id = id).first()
    if team:
        return make_response(team_schema.dump(team), 200)

    abort(404, description='Team not found!')

@routes.post('/team')
@validate()
def create_team(body: PostTeam):
    body = body.dict()
    team = Team(name = body['name'], created = body['created'])
    db.session.add(team)
    db.session.commit()
    return make_response(team_schema.dump(team), 201)

@routes.put('/team/<int:id>')
@validate()
def update_team(id, body: UpdateTeam):
    team = Team.query.filter_by(id = id).first()
    if team:
        body = body.dict()
        if body.get('name'):
            team.name = body['name']
        if body.get('created'):
            team.created = body['created']
        db.session.commit()
        return make_response(team_schema.dump(team), 200)

    abort(404, description='Team not found!')

@routes.delete('/team/<int:id>')
def delete_team(id):
    team = Team.query.filter_by(id = id).first()
    if team:
        db.session.delete(team)
        db.session.commit()
        return make_response(jsonify({"message": "Team deleted!"}), 200)

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

@routes.put('/team/<int:t_id>/coach/<int:c_id>')
def add_team_coach(t_id, c_id):
    team = Team.query.filter_by(id = t_id).first()
    if team:
        coach = Coach.query.filter_by(id = c_id).first()
        if coach:
            if team.coach != coach:
                team.coach = coach
                db.session.commit()
                return make_response(team_schema.dump(team), 200)

            abort(400, description="Coach already in this team!")
        abort(404, description='Coach not found!')
    abort(404, description='Team not found!')
    

@routes.delete('/team/<int:t_id>/coach/<int:c_id>')
def delete_team_coach(t_id, c_id):
    team = Team.query.filter_by(id = t_id).first()
    if team:
        coach = Coach.query.filter_by(id = c_id).first()
        if coach:
            if team.coach == coach:
                team.coach = None
                db.session.commit()
                abort(400, description="Coach is not in this team!")
        abort(404, description='Coach not found!')
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

#Coach
@routes.get('/coach')
def get_coachs():
    coachs = Coach.query.all()
    if coachs:
        return make_response(coachs_schema.dump(coachs), 200)

    abort(404, description='Coachs not found!')

@routes.get('/coach/<int:id>')
def get_coach(id):
    coach = Coach.query.filter_by(id = id).first()
    if coach:
        return make_response(coach_schema.dump(coach), 200)

    abort(404, description='Coach not found!')

@routes.post('/coach')
@validate()
def create_coach(body: PostCoach):
    body = body.dict()
    coach = Coach(name = body['name'], birthdate = body['birthdate'])
    db.session.add(coach)
    db.session.commit()
    return make_response(coach_schema.dump(coach), 201)

@routes.put('/coach/<int:id>')
@validate()
def update_coach(id, body: UpdateCoach):
    coach = Coach.query.filter_by(id = id).first()
    if coach:
        body = body.dict()
        if body.get('name'):
            coach.name = body['name']
        if body.get('birthdate'):
            coach.birthdate = body['birthdate']
        db.session.commit()
        return make_response(coach_schema.dump(coach), 200)

    abort(404, description='Coach not found!')

@routes.delete('/coach/<int:id>')
def delete_coach(id):
    coach = Coach.query.filter_by(id = id).first()
    if coach:
        db.session.delete(coach)
        db.session.commit()
        return make_response(jsonify({"message": "Coach deleted!"}), 200)

    abort(404, description='Coach not found!')
