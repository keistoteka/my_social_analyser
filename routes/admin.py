from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.admin import Admin
from models.user import User
from app import db
from services.auth_service import AuthService
from flask_mail import Message
from datetime import datetime, timedelta

admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Admin):
            flash('Jums nėra leidimo pasiekti šį puslapį', 'error')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and isinstance(current_user, Admin):
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and check_password_hash(admin.password, password):
            login_user(admin)
            flash('Sėkmingai prisijungėte', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Neteisingas vartotojo vardas arba slaptažodis', 'error')
            
    return render_template('admin/login.html')

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sėkmingai atsijungėte', 'success')
    return redirect(url_for('admin.login'))

@admin.route('/')
@login_required
@admin_required
def dashboard():
    users = User.query.all()
    return render_template('admin/dashboard.html', users=users)

@admin.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/users/<int:user_id>/verify', methods=['POST'])
@login_required
@admin_required
def verify_user(user_id):
    user = db.session.get(User, user_id)
    user.is_verified = True
    db.session.commit()
    AuthService.send_verification_email(user)
    flash(f'Vartotojas {user.username} sėkmingai patvirtintas', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/users/<int:user_id>/unverify', methods=['POST'])
@login_required
@admin_required
def unverify_user(user_id):
    user = db.session.get(User, user_id)
    user.is_verified = False
    db.session.commit()
    flash(f'Vartotojo {user.username} patvirtinimas atšauktas', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = db.session.get(User, user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Vartotojas sėkmingai ištrintas', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/create-admin', methods=['GET', 'POST'])
@login_required
@admin_required
def create_admin():
    if not current_user.is_super_admin:
        flash('Jums nėra leidimo kurti administratorius', 'error')
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        is_super_admin = bool(request.form.get('is_super_admin'))
        
        if Admin.query.filter_by(username=username).first():
            flash('Toks vartotojo vardas jau egzistuoja', 'error')
            return redirect(url_for('admin.create_admin'))
            
        if Admin.query.filter_by(email=email).first():
            flash('Toks el. pašto adresas jau egzistuoja', 'error')
            return redirect(url_for('admin.create_admin'))
            
        new_admin = Admin(
            username=username,
            email=email,
            password=generate_password_hash(password),
            is_super_admin=is_super_admin
        )
        
        db.session.add(new_admin)
        db.session.commit()
        flash('Administratorius sėkmingai sukurtas', 'success')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('admin/create_admin.html')

@admin.route('/remove-unverified-users', methods=['POST'])
@login_required
@admin_required
def remove_unverified_users():
    success, message = AuthService.remove_unverified_users()
    flash(message, 'success' if success else 'error')
    return redirect(url_for('admin.dashboard'))

@admin.route('/check-email/<email>')
@login_required
@admin_required
def check_email(email):
    in_use = AuthService.is_email_in_use(email)
    return jsonify({'in_use': in_use})

@admin.route('/message-user', methods=['GET', 'POST'])
@login_required
@admin_required
def message_user():
    users = User.query.all()
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        subject = request.form.get('subject')
        message = request.form.get('message')
        user = db.session.get(User, user_id)
        if not user:
            flash('Vartotojas nerastas', 'error')
            return redirect(url_for('admin.message_user'))
        msg = Message(subject, recipients=[user.email])
        msg.body = message
        from app import mail
        mail.send(msg)
        flash(f'Pranešimas išsiųstas vartotojui {user.username}', 'success')
        return redirect(url_for('admin.message_user'))
    return render_template('admin/message_user.html', users=users)

@admin.route('/users/<int:user_id>/activate-premium', methods=['POST'])
@login_required
@admin_required
def activate_premium(user_id):
    user = db.session.get(User, user_id)
    user.premium_until = datetime.utcnow() + timedelta(days=3)
    db.session.commit()
    flash(f'Vartotojui {user.username} premium aktyvuotas 3 dienoms.', 'success')
    return redirect(url_for('admin.users')) 