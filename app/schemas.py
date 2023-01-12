from . import ma
from .models import User, Team, Player

# Models Schemas
class PlayerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Player
        fields = ('name', 'age', 'weight', 'height', 'position', 'games_played', 'minutes_played', 'cards_yellow', 'cards_red', 'goals', 'team_id', 'id')

class TeamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Team
        exclude = ('created_date', 'id')
    
    players_owned = ma.Nested(PlayerSchema, many = True)

class LoginSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ('username', 'public_id')
    
    teams = ma.Nested(TeamSchema, many = True)
    players_owned = ma.Nested(PlayerSchema, many = True)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('id', 'created_date', 'password_hash', 'last_opening', 'admin')
    
    teams = ma.Nested(TeamSchema, many = True)
    players_owned = ma.Nested(PlayerSchema, many = True)

login_schema = LoginSchema()

user_schema = UserSchema()

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)

player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)
