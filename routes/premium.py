from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app import db

premium_bp = Blueprint('premium', __name__)

@premium_bp.route('/premium', methods=['GET', 'POST'])
@login_required
def premium():
    if current_user.premium_until and current_user.premium_until > datetime.utcnow():
        flash(f'Your premium plan is active until {current_user.premium_until.strftime("%Y-%m-%d")}', 'info')
    if 'plan' in (getattr(request, 'form', {}) or {}):
        plan = request.form.get('plan')
        if plan == '1m':
            current_user.premium_until = datetime.utcnow() + timedelta(days=30)
        elif plan == '3m':
            current_user.premium_until = datetime.utcnow() + timedelta(days=90)
        elif plan == '6m':
            current_user.premium_until = datetime.utcnow() + timedelta(days=180)
        elif plan == '12m':
            current_user.premium_until = datetime.utcnow() + timedelta(days=365)
        else:
            flash('Invalid plan.', 'error')
            return redirect(url_for('premium.premium'))
        db.session.commit()
        flash('Premium plan activated!', 'success')
        return redirect(url_for('premium.premium'))
    return render_template('premium/plans.html') 