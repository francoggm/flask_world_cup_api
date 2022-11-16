from flask import make_response, jsonify, request

from . import app, db
from .models import User, Team, Player, Coach
from .schemas import team_schema, teams_schema, player_schema, players_schema, coach_schema, coachs_schema, serialize_team_relationship

#Teams
@app.get('/team')
def get_teams():
    teams = Team.query.all()
    if teams:
        return make_response(serialize_team_relationship(teams_schema.dump(teams)), 200)
    return make_response(jsonify({"message": "Teams not found!"}), 404)

@app.get('/team/<int:id>')
def get_team(id):
    team = Team.query.filter_by(id = id).first()
    if team:
        return make_response(serialize_team_relationship(team_schema.dump(team)), 200)
    return make_response(jsonify({"message": "Team not found!"}), 404)

@app.post('/team')
def create_team():
    data = request.get_json()
    if data.get('name') and data.get('created_date'):
        team = Team(name = data['name'], created_date = data['created_date'])
        db.session.add(team)
        db.session.commit()
        return make_response(serialize_team_relationship(team_schema.dump(team)), 200)
    return make_response(jsonify({"message": "Wrong informations!"}), 400)

@app.put('/team/<int:id>')
def update_team(id):
    team = Team.query.filter_by(id = id).first()
    if team:
        data = request.get_json()
        if data.get('name'):
            team.name = data['name']
        if data.get('created_date'):
            team.created_date = data['created_date']
        db.session.commit()
        return make_response(serialize_team_relationship(team_schema.dump(team)), 200)
    return make_response(jsonify({"message": "Team not found!"}), 404)

@app.delete('/team/<int:id>')
def delete_team(id):
    team = Team.query.filter_by(id = id).first()
    if team:
        db.session.delete(team)
        db.session.commit()
        return make_response(jsonify({"message": "Team deleted!"}), 200)
    return make_response(jsonify({"message": "Team not found!"}), 404)

@app.put('/team-player')
def add_team_player():
    data = request.get_json()
    if data.get('team_id') and data.get('player_id'):
        team = Team.query.filter_by(id = int(data['team_id'])).first()
        if team:
            player = Player.query.filter_by(id = int(data['player_id'])).first()
            if player:
                if not player in team.players:
                    team.players.append(player)
                    db.session.commit()
                    return make_response(serialize_team_relationship(team_schema.dump(team)), 200)
                return make_response(jsonify({"message": "Player already in this team!"}), 400)
            return make_response(jsonify({"message": "Player not found!"}), 404)
        return make_response(jsonify({"message": "Team not found!"}),404)
    return make_response(jsonify({"message": "Wrong informations!"}), 400)

@app.delete('/team-player')
def delete_team_player():
    data = request.get_json()
    if data.get('team_id') and data.get('player_id'):
        team = Team.query.filter_by(id = int(data['team_id'])).first()
        if team:
            player = Player.query.filter_by(id = int(data['player_id'])).first()
            if player:
                if player in team.players:
                    team.players.remove(player)
                    db.session.commit()
                    return make_response(serialize_team_relationship(team_schema.dump(team)), 200)
                return make_response(jsonify({"message": "Player is not in this team!"}), 400)
            return make_response(jsonify({"message": "Player not found!"}), 404)
        return make_response(jsonify({"message": "Team not found!"}),404)
    return make_response(jsonify({"message": "Wrong informations!"}), 400)

@app.put('/team-coach')
def add_team_coach():
    data = request.get_json()
    if data.get('team_id') and data.get('coach_id'):
        team = Team.query.filter_by(id = int(data['team_id'])).first()
        if team:
            coach = Coach.query.filter_by(id = int(data['coach_id'])).first()
            if coach:
                if team.coach != coach:
                    team.coach = coach
                    db.session.commit()
                    return make_response(serialize_team_relationship(team_schema.dump(team)), 200)
                return make_response(jsonify({"message": "Coach already in this team!"}), 400)
            return make_response(jsonify({"message": "Coach not found!"}), 404)
        return make_response(jsonify({"message": "Team not found!"}),404)
    return make_response(jsonify({"message": "Wrong informations!"}), 400)

@app.delete('/team-coach')
def delete_team_coach():
    data = request.get_json()
    if data.get('team_id') and data.get('coach_id'):
        team = Team.query.filter_by(id = int(data['team_id'])).first()
        if team:
            coach = Coach.query.filter_by(id = int(data['coach_id'])).first()
            if coach:
                if team.coach == coach:
                    team.coach = None
                    db.session.commit()
                    return make_response(serialize_team_relationship(team_schema.dump(team)), 200)
                return make_response(jsonify({"message": "Coach is not in this team!"}), 400)
            return make_response(jsonify({"message": "Coach not found!"}), 404)
        return make_response(jsonify({"message": "Team not found!"}),404)
    return make_response(jsonify({"message": "Wrong informations!"}), 400)

#Players
@app.get('/player')
def get_players():
    players = Player.query.all()
    if players:
        return make_response(players_schema.dump(players), 200)
    return make_response(jsonify({"message": "Players not found!"}), 404)

@app.get('/player/<int:id>')
def get_player(id):
    player = Player.query.filter_by(id = id).first()
    if player:
        return make_response(player_schema.dump(player), 200)
    return make_response(jsonify({"message": "Player not found!"}), 404)

@app.post('/player')
def create_player():
    data = request.get_json()
    if data.get('name') and data.get('age') and data.get('weight') and data.get('height'):
        player = Player(name = data['name'], age = data['age'], weight = data['weight'], height = data['height'])
        db.session.add(player)
        db.session.commit()
        return make_response(player_schema.dump(player), 200)
    return make_response(jsonify({"message": "Wrong informations!"}), 404)

@app.put('/player/<int:id>')
def update_player(id):
    player = Player.query.filter_by(id = id).first()
    if player:
        data = request.get_json()
        if data.get('name'):
            player.name = data['name']
        if data.get('age'):
            player.age = data['age']
        if data.get('weight'):
            player.weight = float(data['weight'])
        if data.get('height'):
            player.height = int(data['height'])
        db.session.commit()
        return make_response(player_schema.dump(player), 200)
    return make_response(jsonify({"message": "Player not found!"}), 404)

@app.delete('/player/<int:id>')
def delete_player(id):
    player = Player.query.filter_by(id = id).first()
    if player:
        db.session.delete(player)
        db.session.commit()
        return make_response(jsonify({"message": "Player deleted!"}), 200)
    return make_response(jsonify({"message": "Player not found!"}), 404)

#Coach
@app.get('/coach')
def get_coachs():
    coachs = Coach.query.all()
    if coachs:
        return make_response(coachs_schema.dump(coachs), 200)
    return make_response(jsonify({"message": "Coachs not found!"}), 404)

@app.get('/coach/<int:id>')
def get_coach(id):
    coach = Coach.query.filter_by(id = id).first()
    if coach:
        return make_response(coach_schema.dump(coach), 200)
    return make_response(jsonify({"message": "Coach not found!"}), 404)

@app.post('/coach')
def create_coach():
    data = request.get_json()
    if data.get('name') and data.get('age'):
        coach = Coach(name = data['name'], age = data['age'])
        db.session.add(coach)
        db.session.commit()
        return make_response(coach_schema.dump(coach), 200)
    return make_response(jsonify({"message": "Wrong informations!"}), 404)

@app.put('/coach/<int:id>')
def update_coach(id):
    coach = Coach.query.filter_by(id = id).first()
    if coach:
        data = request.get_json()
        if data.get('name'):
            coach.name = data['name']
        if data.get('age'):
            coach.age = data['age']
        db.session.commit()
        return make_response(coach_schema.dump(coach), 200)
    return make_response(jsonify({"message": "Coach not found!"}), 404)

@app.delete('/coach/<int:id>')
def delete_coach(id):
    coach = Coach.query.filter_by(id = id).first()
    if coach:
        db.session.delete(coach)
        db.session.commit()
        return make_response(jsonify({"message": "Coach deleted!"}), 200)
    return make_response(jsonify({"message": "Coach not found!"}), 404)
