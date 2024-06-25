from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    reports = db.relationship('Report', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(140))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    damage_type = db.Column(db.String(50))
    problem_media = db.relationship('ProblemMedia', backref='report', lazy=True)
    damage_media = db.relationship('DamageMedia', backref='report', lazy=True)

    def __repr__(self):
        return '<Report {}>'.format(self.description)

class Damage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'))
    description = db.Column(db.String(140))
    cost = db.Column(db.Float)

    def __repr__(self):
        return '<Damage {}>'.format(self.description)

class TrafficControl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    control_type = db.Column(db.String(50))  # Ex: Radar, Quebra-mola, etc.

    def __repr__(self):
        return '<TrafficControl {}>'.format(self.description)
    
class ProblemMedia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'))
    file_path = db.Column(db.String(200))

class DamageMedia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'))
    file_path = db.Column(db.String(200))