from . import ma
from .models import User, Team, Player, Coach

# Models Schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ('username', 'public_id')

class PlayerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Player
        fields = ('name', 'age', 'weight', 'height', 'team_id', 'id')

class CoachSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Coach
        fields = ('name', 'age', 'team_id', 'id')

class TeamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Team

    players = ma.Nested(PlayerSchema, many=True)
    coach = ma.Nested(CoachSchema)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)

player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)

coach_schema = CoachSchema()
coachs_schema = CoachSchema(many=True)