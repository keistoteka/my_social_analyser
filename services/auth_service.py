from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from app import db
from models.social_connection import UserSocialConnection
from flask_mail import Mail, Message
from app import mail

class AuthService:
    @staticmethod
    def register_user(username, email, password):
        if User.query.filter_by(username=username).first():
            return False, 'Toks vartotojo vardas jau egzistuoja'
        
        if User.query.filter_by(email=email).first():
            return False, 'Toks el. pašto adresas jau egzistuoja'
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return True, 'Registracija sėkminga!'
        except Exception as e:
            db.session.rollback()
            return False, 'Įvyko klaida. Bandykite dar kartą.'

    @staticmethod
    def verify_user(email, password):
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return user
        return None

    @staticmethod
    def change_password(user, current_password, new_password):
        if not check_password_hash(user.password, current_password):
            return False, 'Neteisingas dabartinis slaptažodis'
        
        user.password = generate_password_hash(new_password)
        try:
            db.session.commit()
            return True, 'Slaptažodis sėkmingai atnaujintas'
        except Exception as e:
            db.session.rollback()
            return False, 'Įvyko klaida. Bandykite dar kartą.'

    @staticmethod
    def delete_account(user):
        try:
            # Delete all social connections for this user
            UserSocialConnection.query.filter_by(user_id=user.id).delete()
            db.session.delete(user)
            db.session.commit()
            return True, 'Paskyra sėkmingai ištrinta'
        except Exception as e:
            db.session.rollback()
            return False, 'Įvyko klaida. Bandykite dar kartą.'

    @staticmethod
    def remove_unverified_users():
        try:
            unverified_users = User.query.filter(User.is_verified == 0).all()
            for user in unverified_users:
                # Delete all social connections
                UserSocialConnection.query.filter_by(user_id=user.id).delete()
                # Delete all social profiles (if used)
                if hasattr(user, 'social_profiles'):
                    for profile in user.social_profiles:
                        db.session.delete(profile)
                db.session.delete(user)
            db.session.commit()
            return True, f'Removed {len(unverified_users)} unverified users.'
        except Exception as e:
            db.session.rollback()
            return False, 'Error while removing unverified users.'

    @staticmethod
    def is_email_in_use(email):
        return User.query.filter_by(email=email).first() is not None

    @staticmethod
    def send_verification_email(user):
        msg = Message('Jūsų paskyra patvirtinta', sender='noreply@example.com', recipients=[user.email])
        msg.body = f'Sveiki {user.username},\n\nJūsų paskyra buvo patvirtinta. Dabar galite prisijungti.'
        mail.send(msg) 