from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
from extensions import db, login_manager, oauth, mail
from flask_mail import Mail
from flask_migrate import Migrate

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///digital_footprint.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Email configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    oauth.init_app(app)
    mail.init_app(app)
    app.config['FACEBOOK_CLIENT_ID'] = os.getenv('FACEBOOK_CLIENT_ID', 'your-facebook-app-id')
    app.config['FACEBOOK_CLIENT_SECRET'] = os.getenv('FACEBOOK_CLIENT_SECRET', 'your-facebook-app-secret')
    app.config['LINKEDIN_CLIENT_ID'] = os.getenv('LINKEDIN_CLIENT_ID', 'your-linkedin-client-id')
    app.config['LINKEDIN_CLIENT_SECRET'] = os.getenv('LINKEDIN_CLIENT_SECRET', 'your-linkedin-client-secret')
    app.config['INSTAGRAM_CLIENT_ID'] = os.getenv('INSTAGRAM_CLIENT_ID', 'your-instagram-client-id')
    app.config['INSTAGRAM_CLIENT_SECRET'] = os.getenv('INSTAGRAM_CLIENT_SECRET', 'your-instagram-client-secret')
    oauth.register(
        name='facebook',
        client_id=app.config['FACEBOOK_CLIENT_ID'],
        client_secret=app.config['FACEBOOK_CLIENT_SECRET'],
        access_token_url='https://graph.facebook.com/v10.0/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/v10.0/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/v10.0/',
        client_kwargs={'scope': 'email public_profile'},
    )
    oauth.register(
        name='linkedin',
        client_id=os.getenv('LINKEDIN_CLIENT_ID'),
        client_secret=os.getenv('LINKEDIN_CLIENT_SECRET'),
        access_token_url='https://www.linkedin.com/oauth/v2/accessToken',
        access_token_params=None,
        authorize_url='https://www.linkedin.com/oauth/v2/authorization',
        authorize_params=None,
        api_base_url='https://api.linkedin.com/v2/',
        client_kwargs={'scope': 'r_liteprofile r_emailaddress'},
    )
    oauth.register(
        name='instagram',
        client_id=os.getenv('INSTAGRAM_CLIENT_ID'),
        client_secret=os.getenv('INSTAGRAM_CLIENT_SECRET'),
        access_token_url='https://api.instagram.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://api.instagram.com/oauth/authorize',
        authorize_params=None,
        api_base_url='https://graph.instagram.com/',
        client_kwargs={'scope': 'user_profile,user_media'},
    )
    
    # Register blueprints
    from routes.auth import auth
    from routes.main import main
    from routes.admin import admin
    from routes.premium import premium_bp
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(premium_bp)
    
    # User loader
    from models.user import User
    from models.admin import Admin
    
    @login_manager.user_loader
    def load_user(user_id):
        if user_id.startswith('admin-'):
            admin_id = int(user_id.split('-')[1])
            return db.session.get(Admin, admin_id)
        elif user_id.startswith('user-'):
            user_id_int = int(user_id.split('-')[1])
            return db.session.get(User, user_id_int)
        return None
    
    migrate = Migrate(app, db)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 