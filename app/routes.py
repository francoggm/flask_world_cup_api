from . import app, db
from .models import User, Team, Player, Coach
from .models import team_schema, teams_schema, player_schema, players_schema, coach_schema, coachs_schema

from flask import make_response, jsonify, request

#Teams
@app.route('/team')
def get_teams():
    pass

@app.route('/team/<int:id>')
def get_team(id):
    pass

@app.route('/team/<int:id>', methods=['PUT'])
def update_team(id):
    pass

@app.route('/team/<int:id>', methods=['DELETE'])
def delete_team(id):
    pass

@app.route('/team-player/<int:id>', methods=['PUT'])
def add_player(id):
    pass

@app.route('/team-player/<int:id>', methods=['DELETE'])
def delete_player(id):
    pass

@app.route('/team-coach/<int:id>', methods=['PUT'])
def add_coach(id):
    pass

@app.route('/team-coach/<int:id>', methods=['DELETE'])
def delete_coach(id):
    pass

#Players
@app.route('/player')
def get_players():
    pass

@app.route('/player/<int:id>')
def get_player(id):
    pass

@app.route('/player/<int:id>', methods=['PUT'])
def update_player(id):
    pass

@app.route('/player/<int:id>', methods=['DELETE'])
def delete_player(id):
    pass

#Coach
@app.route('/coach')
def get_coachs():
    pass

@app.route('/coach/<int:id>')
def get_coach(id):
    pass

@app.route('/coach/<int:id>', methods=['PUT'])
def update_coach(id):
    pass

@app.route('/coach/<int:id>', methods=['DELETE'])
def delete_coach(id):
    pass