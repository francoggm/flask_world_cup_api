from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
from sqlalchemy.sql import func

from . import db

user_player = db.Table('user_player',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
)

user_coach = db.Table('user_coach',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('coach_id', db.Integer, db.ForeignKey('coach.id'), primary_key=True)
)

player_team = db.Table('player_team',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True)
)

coach_team = db.Table('coach_team',
    db.Column('coach_id', db.Integer, db.ForeignKey('coach.id'), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True)
)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)
    admin = db.Column(db.Boolean(), default=False)
    created_date = db.Column(db.DateTime(), default=func.now())
    
    players = db.relationship('Player', secondary = 'user_player', overlaps='players')
    coachs = db.relationship('Coach', secondary = 'user_coach', overlaps='coachs')
    teams = db.relationship('Team', backref = 'user')

    @property
    def password(self):
        return self.password_hash
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, 'sha256')
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self) -> str:
        return f'{self.username}, Admin: {self.admin}'

class Player(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    birthdate = db.Column(db.Date())
    weight = db.Column(db.Numeric(precision=5, scale=2), nullable=False)
    height = db.Column(db.Integer(), nullable=False)
    
    users = db.relationship(User, secondary = 'user_player', overlaps='players')
    teams = db.relationship('Team', secondary = 'player_team', overlaps='players')

    @property
    def age(self):
        if self.birthdate:
            today = date.today()
            return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        return None
    
    def __repr__(self) -> str:
        return f'{self.name}'

class Coach(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    birthdate = db.Column(db.Date())
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    users = db.relationship(User, secondary = 'user_coach', overlaps='coachs')
    teams = db.relationship('Team', secondary = 'coach_team', overlaps='coachs')

    @property
    def age(self):
        if self.birthdate:
            today = date.today()
            return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        return None
    
    def __repr__(self) -> str:
        return f'{self.name}'

class Team(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    created = db.Column(db.Date(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    players = db.relationship(Player, secondary = 'player_team', overlaps='players')
    coachs = db.relationship(Coach, secondary = 'coach_team', overlaps='coachs')

    def __repr__(self) -> str:
        return f'Team {self.name}'



