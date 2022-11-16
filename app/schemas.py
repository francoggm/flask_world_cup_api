from . import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('public_id','username', 'admin', 'created_date')

class PlayerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'age', 'weight', 'height', 'team_id')

class CoachSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'age', 'team_id')

class TeamSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'created_date', 'coach', 'players')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)

player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)

coach_schema = CoachSchema()
coachs_schema = CoachSchema(many=True)

def serialize_team_relationship(team_schema):
    if isinstance(team_schema, list):
        for team in team_schema:
            if team.get('players'):
                team['players'] = players_schema.dump(team['players'])
            if team.get('coach'):
                team['coach'] = coach_schema.dump(team['coach'])
    else:
        if team_schema.get('players'):
            team_schema['players'] = players_schema.dump(team_schema['players'])
        if team_schema.get('coach'):
            team_schema['coach'] = coach_schema.dump(team_schema['coach'])
    return team_schema
