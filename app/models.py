from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
from sqlalchemy.sql import func

from . import db, ma

# Models

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    public_id = db.Column(db.String(12), unique=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)
    admin = db.Column(db.Boolean(), default=False)
    created_date = db.Column(db.DateTime(), default=func.now())

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

class Team(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    created = db.Column(db.Date())
    coach = db.relationship('Coach', backref='coach', uselist=False)
    players = db.relationship('Player', backref='player')

    @property
    def created_date(self):
        if self.created:
            return self.created.strftime('%Y/%m/%d')
        return None
    
    @created_date.setter
    def created_date(self, string_date):
        date_list = string_date.split('/')
        self.created = date(int(date_list[0]), int(date_list[1]), int(date_list[2])) 

    def __repr__(self) -> str:
        return f'Team {self.name}'

class Player(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    birthdate = db.Column(db.Date())
    weight = db.Column(db.Numeric(precision=5, scale=2))
    height = db.Column(db.Integer())
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    @property
    def age(self):
        if self.birthdate:
            today = date.today()
            return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        return None
    
    @age.setter
    def age(self, string_date):
        date_list = string_date.split('/')
        self.birthdate = date(int(date_list[0]), int(date_list[1]), int(date_list[2])) 
    
    def __repr__(self) -> str:
        return f'{self.name}'

class Coach(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    birthdate = db.Column(db.Date())
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    @property
    def age(self):
        if self.birthdate:
            today = date.today()
            return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        return None
    
    @age.setter
    def age(self, string_date):
        date_list = string_date.split('/')
        self.birthdate = date(int(date_list[0]), int(date_list[1]), int(date_list[2])) 
    
    def __repr__(self) -> str:
        return f'{self.name}'

# Schemas

class UserSchema(ma.Schema):
    class Meta:
        fields = ('public_id','username', 'admin', 'created_date')

class TeamSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'created_date', 'coach', 'players')

class PlayerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'age', 'weight', 'height', 'team_id')

class CoachSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'age', 'team_id')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)

player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)

coach_schema = CoachSchema()
coachs_schema = CoachSchema(many=True)


