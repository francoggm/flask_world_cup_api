from . import ma
from .models import User, Team, Player, UserCollection

# Models Schemas
class UserCollectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserCollection
        fields = ('player_id', 'team_id')

class PlayerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Player
        fields = ('name', 'age', 'weight', 'height', 'role', 'team_id', 'id')

class TeamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Team
        exclude = ('created_date',)

    players = ma.Nested(UserCollectionSchema, many=True)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ('username', 'public_id')
    
    teams = ma.Nested(TeamSchema, many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)

player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)
