from flask import request, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
import os
import urllib.parse

db = SQLAlchemy()

LINKEDIN_CLIENT_ID = os.environ.get('LINKEDIN_CLIENT_ID')
LINKEDIN_CLIENT_SECRET = os.environ.get('LINKEDIN_CLIENT_SECRET')
LINKEDIN_REDIRECT_URI = os.environ.get('LINKEDIN_REDIRECT_URI')  # e.g. http://localhost:5000/auth/linkedin/callback

@auth_bp.route('/linkedin-login')
def linkedin_login():
    base_url = "https://www.linkedin.com/oauth/v2/authorization"
    params = {
        "response_type": "code",
        "client_id": LINKEDIN_CLIENT_ID,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
        "scope": "r_liteprofile r_emailaddress"
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return redirect(url)

@auth_bp.route('/linkedin/callback')
def linkedin_callback():
    code = request.args.get('code')
    error = request.args.get('error')
    if error:
        return f"LinkedIn error: {error}", 400
    if not code:
        return "No code provided", 400
    # TODO: Exchange code for access token and fetch user info
    return f"Received code: {code} (implement token exchange here)", 200

@auth_bp.route('/linkedin-accounts')
@login_required
def linkedin_accounts():
    accounts = LinkedInAccount.query.filter_by(user_id=current_user.id).all()
    return jsonify({
        'success': True,
        'accounts': [{
            'id': acc.id,
            'email': acc.email,
            'profile_name': acc.profile_name,
            'last_used': acc.last_used.isoformat() if acc.last_used else None
        } for acc in accounts]
    })

@auth_bp.route('/linkedin-account/<int:account_id>/disconnect', methods=['POST'])
@login_required
def disconnect_linkedin_account(account_id):
    account = LinkedInAccount.query.filter_by(
        id=account_id,
        user_id=current_user.id
    ).first()
    
    if not account:
        return jsonify({
            'success': False,
            'message': 'LinkedIn account not found'
        })
    
    try:
        db.session.delete(account)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'LinkedIn account disconnected successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error disconnecting LinkedIn account: {str(e)}'
        }) 