from extensions import db
from datetime import datetime

class UserSocialConnection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    connected_at = db.Column(db.DateTime, default=datetime.utcnow)
    analysis_options = db.Column(db.Text)  # JSON string of options
    save_credentials = db.Column(db.Boolean, default=False)
    credentials = db.Column(db.Text)  # JSON string: {"email": ..., "password": ...}
    access_token = db.Column(db.Text)  # OAuth access token for the platform

    def __repr__(self):
        return f'<UserSocialConnection user_id={self.user_id} platform={self.platform}>' 