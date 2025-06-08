from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
import json
from models.social_connection import UserSocialConnection
from extensions import db
from services.analysis_service import AnalysisService

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        if hasattr(current_user, 'is_super_admin') and getattr(current_user, 'is_super_admin', False):
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    connections = UserSocialConnection.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', connections=connections)

@main.route('/analyze')
@login_required
def analyze():
    platforms = ['twitter', 'facebook', 'instagram', 'linkedin']
    connections = {c.platform: c for c in UserSocialConnection.query.filter_by(user_id=current_user.id).all()}
    return render_template('analyze.html', platforms=platforms, connections=connections)

@main.route('/connect-social', methods=['POST'])
@login_required
def connect_social():
    platform = request.form.get('platform')
    analysis_options = request.form.getlist('analysis_options')
    email = request.form.get('email')
    password = request.form.get('password')
    save_credentials = bool(request.form.get('save_credentials'))
    if not platform or not analysis_options:
        flash('Please select a platform and at least one analysis option.', 'error')
        return redirect(url_for('main.analyze'))
    credentials = None
    if save_credentials:
        credentials = json.dumps({'email': email, 'password': password})
    # Remove previous connection for this user/platform
    UserSocialConnection.query.filter_by(user_id=current_user.id, platform=platform).delete()
    conn = UserSocialConnection(
        user_id=current_user.id,
        platform=platform,
        analysis_options=json.dumps(analysis_options),
        save_credentials=save_credentials,
        credentials=credentials
    )
    db.session.add(conn)
    db.session.commit()
    flash('Successfully connected to {} with selected analysis options!'.format(platform.capitalize()), 'success')
    return redirect(url_for('main.analyze'))

@main.route('/disconnect-social', methods=['POST'])
@login_required
def disconnect_social():
    platform = request.form.get('platform')
    conn = UserSocialConnection.query.filter_by(user_id=current_user.id, platform=platform).first()
    if conn:
        conn.credentials = None
        conn.save_credentials = False
        db.session.commit()
        flash('Disconnected from {}.'.format(platform.capitalize()), 'success')
    else:
        flash('No connection found for {}.'.format(platform.capitalize()), 'error')
    return redirect(url_for('main.analyze'))

# --- Sentimentų analizės pavyzdys ---
@main.route('/sentiment-demo')
@login_required
def sentiment_demo():
    texts = request.args.getlist('text') or [
        'I love this!',
        'This is terrible.',
        'It is okay, not great.',
        'Amazing experience!',
        'I hate this.'
    ]
    analysis = AnalysisService()
    sentiment_df = analysis.sentiment_analysis(texts)
    fig = analysis.plot_sentiment(sentiment_df)
    import io, base64
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return render_template('sentiment_demo.html', img_base64=img_base64, texts=texts, sentiment=sentiment_df.to_dict(orient='records')) 