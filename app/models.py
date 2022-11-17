from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
from sqlalchemy.sql import func

from . import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
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
    created = db.Column(db.Date(), nullable=False)
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
    weight = db.Column(db.Numeric(precision=5, scale=2), nullable=False)
    height = db.Column(db.Integer(), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

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

    @property
    def age(self):
        if self.birthdate:
            today = date.today()
            return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        return None
    
    def __repr__(self) -> str:
        return f'{self.name}'



