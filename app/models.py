from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    save_codes = db.relationship('SaveCode', backref='coder', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)    

class SaveCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_code = db.Column(db.String(10000))
    timestamp = db.Column(db.Integer, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<SaveCode {}>'.format(self.source_code)