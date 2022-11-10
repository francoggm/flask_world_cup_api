from werkzeug.security import check_password_hash, generate_password_hash

from . import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)
    admin = db.Column(db.Boolean(), default=False)

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
    player = db.relationship('Player', backref='player')

class Player(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    age = db.Column(db.Date())
    weight = db.Column(db.Numeric(precision=5, scale=2))
    height = db.Column(db.Integer())
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

class Coach(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    age = db.Column(db.Date())
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))