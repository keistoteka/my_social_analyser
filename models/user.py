from flask_login import UserMixin
from datetime import datetime
from extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    social_profiles = db.relationship('SocialProfile', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def get_id(self):
        return f'user-{self.id}'

class SocialProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    last_analyzed = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 