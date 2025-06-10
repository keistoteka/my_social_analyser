from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from forms.auth import LoginForm, RegistrationForm, ChangePasswordForm
from services.auth_service import AuthService
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from extensions import db, oauth, mail
from models.social_connection import UserSocialConnection
import requests
import os
from flask_mail import Message

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    values = {'username': '', 'email': ''}
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm-password', '')
        terms = request.form.get('terms')
        values = {'username': username, 'email': email}

        # Validation
        if not username or not email or not password or not confirm_password:
            flash('All fields are required.', 'error')
        elif password != confirm_password:
            flash('Passwords do not match.', 'error')
        elif not terms:
            flash('You must agree to the Terms and Conditions.', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
        else:
            # Registration successful
            user = User(username=username, email=email, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            # Send registration email
            try:
                msg = Message(
                    subject="Registration Successful",
                    recipients=[email],
                    body="Sveikiname! Jūsų registracija sėkminga. Laukite administratoriaus patvirtinimo."
                )
                mail.send(msg)
            except Exception as e:
                print('Nepavyko išsiųsti el. laiško:', e)
            flash('Registration successful! Please wait for admin approval before logging in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('register.html', values=values)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    email = ''
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            if not user.is_verified:
                flash('Your account is not yet approved by admin.', 'error')
                return render_template('login.html', email=email)
            login_user(user, remember=remember)
            flash('Successfully logged in!', 'success')
            # Redirect admin to admin panel, user to dashboard
            if hasattr(user, 'is_super_admin') and getattr(user, 'is_super_admin', False):
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password.', 'error')
            return render_template('login.html', email=email)

    return render_template('login.html', email=email)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sėkmingai atsijungėte', 'success')
    return redirect(url_for('main.index'))

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Check if username or email is already taken by another user
        if username != current_user.username:
            if User.query.filter_by(username=username).first():
                flash('Toks vartotojo vardas jau egzistuoja', 'error')
                return redirect(url_for('auth.profile'))

        if email != current_user.email:
            if User.query.filter_by(email=email).first():
                flash('Toks el. pašto adresas jau egzistuoja', 'error')
                return redirect(url_for('auth.profile'))

        # Update user information
        current_user.username = username
        current_user.email = email

        # If changing password
        if current_password and new_password:
            if not check_password_hash(current_user.password, current_password):
                flash('Neteisingas dabartinis slaptažodis', 'error')
                return redirect(url_for('auth.profile'))

            if new_password != confirm_password:
                flash('Nauji slaptažodžiai nesutampa', 'error')
                return redirect(url_for('auth.profile'))

            current_user.password = generate_password_hash(new_password)

        db.session.commit()
        flash('Profilis sėkmingai atnaujintas', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('profile.html')

@auth.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    success, message = AuthService.delete_account(current_user)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('main.index'))

@auth.route('/login/facebook')
def facebook_login():
    redirect_uri = url_for('auth.facebook_callback', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)

@auth.route('/login/facebook/callback')
def facebook_callback():
    token = oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get('me?fields=id,name,email')
    profile = resp.json()
    email = profile.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        # Optionally, auto-register user or show error
        flash('No user found with this Facebook email. Please register first.', 'error')
        return redirect(url_for('auth.login'))
    if not user.is_verified:
        flash('Your account is not yet approved by admin.', 'error')
        return redirect(url_for('auth.login'))
    login_user(user)
    flash('Successfully logged in with Facebook!', 'success')
    # Check if user wants to save credentials (from session)
    remember_creds = session.pop('remember_facebook_creds', False)
    if remember_creds:
        # Save or update token in UserSocialConnection
        conn = UserSocialConnection.query.filter_by(user_id=user.id, platform='facebook').first()
        if not conn:
            conn = UserSocialConnection(user_id=user.id, platform='facebook')
            db.session.add(conn)
        conn.access_token = token['access_token']
        conn.connected_at = db.func.now()
        db.session.commit()
    return redirect(url_for('main.dashboard'))

@auth.route('/login/linkedin')
def linkedin_login():
    redirect_uri = url_for('auth.linkedin_callback', _external=True)
    return oauth.linkedin.authorize_redirect(redirect_uri)

@auth.route('/login/linkedin/callback')
def linkedin_callback():
    try:
        token = oauth.linkedin.authorize_access_token()
        resp = oauth.linkedin.get('me')
        profile = resp.json()
        email_resp = oauth.linkedin.get('emailAddress?q=members&projection=(elements*(handle~))')
        email_data = email_resp.json()
        email = None
        if 'elements' in email_data and email_data['elements']:
            email = email_data['elements'][0]['handle~']['emailAddress']
        if not email:
            flash('Could not retrieve email from LinkedIn.', 'error')
            return redirect(url_for('auth.login'))
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('No user found with this LinkedIn email. Please register first.', 'error')
            return redirect(url_for('auth.login'))
        login_user(user)
        flash('Successfully logged in with LinkedIn!', 'success')
        # (optional) išsaugok access_token, jei reikia
        return redirect(url_for('main.dashboard'))
    except Exception as e:
        flash('LinkedIn login failed. Please try again.', 'error')
        return redirect(url_for('auth.login'))

@auth.route('/login/instagram')
def instagram_login():
    redirect_uri = url_for('auth.instagram_callback', _external=True)
    return oauth.instagram.authorize_redirect(redirect_uri)

@auth.route('/login/instagram/callback')
def instagram_callback():
    try:
        token = oauth.instagram.authorize_access_token()
        resp = oauth.instagram.get('me?fields=id,username')
        profile = resp.json()
        # Instagram Basic Display API does not provide email, so use username as identifier
        username = profile.get('username')
        if not username:
            flash('Could not retrieve Instagram username.', 'error')
            return redirect(url_for('auth.login'))
        user = User.query.filter_by(username=username).first()
        if not user:
            flash('No user found with this Instagram username. Please register first.', 'error')
            return redirect(url_for('auth.login'))
        if not user.is_verified:
            flash('Your account is not yet approved by admin.', 'error')
            return redirect(url_for('auth.login'))
        login_user(user)
        flash('Successfully logged in with Instagram!', 'success')
        # Save or update token in UserSocialConnection
        conn = UserSocialConnection.query.filter_by(user_id=user.id, platform='instagram').first()
        if not conn:
            conn = UserSocialConnection(user_id=user.id, platform='instagram')
            db.session.add(conn)
        conn.access_token = token['access_token']
        conn.connected_at = db.func.now()
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    except Exception as e:
        print('EXCEPTION in Instagram callback:', e)
        flash('Instagram login failed. Please try again.', 'error')
        return redirect(url_for('auth.login'))

@auth.route('/linkedin-login')
def oauth_linkedin_login():
    return redirect(url_for('auth.linkedin_login')) 