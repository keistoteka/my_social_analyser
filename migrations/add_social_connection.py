import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extensions import db
from models.social_connection import UserSocialConnection
from sqlalchemy import inspect, text
from app import create_app

def upgrade():
    app = create_app()
    with app.app_context():
        inspector = inspect(db.engine)
        if not inspector.has_table('user_social_connection'):
            db.create_all()
            print("UserSocialConnection table created successfully!")
        else:
            # Add new columns if they do not exist
            columns = [col['name'] for col in inspector.get_columns('user_social_connection')]
            if 'save_credentials' not in columns:
                db.session.execute(text('ALTER TABLE user_social_connection ADD COLUMN save_credentials BOOLEAN DEFAULT FALSE'))
            if 'credentials' not in columns:
                db.session.execute(text('ALTER TABLE user_social_connection ADD COLUMN credentials TEXT'))
            if 'access_token' not in columns:
                db.session.execute(text('ALTER TABLE user_social_connection ADD COLUMN access_token TEXT'))
            db.session.commit()
            print("UserSocialConnection table already exists. Columns checked/added.")

if __name__ == '__main__':
    upgrade() 