from extensions import db
from flask_login import UserMixin

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_super_admin = db.Column(db.Boolean, default=False)

    def get_id(self):
        return f'admin-{self.id}' 