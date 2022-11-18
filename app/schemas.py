from pydantic import BaseModel
from typing import Optional

from . import ma
from .models import User, Team, Player, Coach

# Response Schemas
class PostAuth(BaseModel):
    username: str
    password: str

class PostUser(BaseModel):
    pass

class PostTeam(BaseModel):
    name: str
    created: str

class PostPlayer(BaseModel):
    name: str
    birthdate: str
    weight: float
    height: int

class PostCoach(BaseModel):
    name: str 
    birthdate: str

class UpdateUser(BaseModel):
    pass

class UpdateTeam(BaseModel):
    name: Optional[str]
    created_date: Optional[str]

class UpdatePlayer(BaseModel):
    name: Optional[str]
    birthdate: Optional[str]
    weight: Optional[float]
    height: Optional[int]

class UpdateCoach(BaseModel):
    name: Optional[str]
    birthdate: Optional[str]

# Models Schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ("password_hash", "id")

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