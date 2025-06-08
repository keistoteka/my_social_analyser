import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from sqlalchemy import text

def upgrade():
    app = create_app()
    with app.app_context():
        # Add new columns to User table
        db.session.execute(text('ALTER TABLE user ADD COLUMN is_verified BOOLEAN DEFAULT FALSE'))
        db.session.execute(text('ALTER TABLE user ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP'))
        db.session.execute(text('UPDATE user SET is_verified = TRUE'))
        db.session.commit()
        print("Database migration completed successfully!")

if __name__ == '__main__':
    upgrade() 