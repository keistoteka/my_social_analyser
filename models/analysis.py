from extensions import db

class EngagementAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    platform = db.Column(db.String(32), nullable=False)
    analyzed_at = db.Column(db.DateTime, nullable=False)
    total_likes = db.Column(db.Integer, default=0)
    total_comments = db.Column(db.Integer, default=0)
    total_shares = db.Column(db.Integer, default=0)
    post_count = db.Column(db.Integer, default=0)

class SentimentAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    platform = db.Column(db.String(32), nullable=False)
    analyzed_at = db.Column(db.DateTime, nullable=False)
    positive_count = db.Column(db.Integer, default=0)
    negative_count = db.Column(db.Integer, default=0)
    neutral_count = db.Column(db.Integer, default=0)
    average_score = db.Column(db.Float, default=0.0)

class GrowthAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    platform = db.Column(db.String(32), nullable=False)
    analyzed_at = db.Column(db.DateTime, nullable=False)
    start_followers = db.Column(db.Integer, default=0)
    end_followers = db.Column(db.Integer, default=0)
    growth_rate = db.Column(db.Float, default=0.0)
    engagement_change = db.Column(db.Float, default=0.0)

class ContentAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    platform = db.Column(db.String(32), nullable=False)
    analyzed_at = db.Column(db.DateTime, nullable=False)
    top_content_type = db.Column(db.String(32))
    top_post_id = db.Column(db.String(64))
    top_post_engagement = db.Column(db.Integer, default=0)
    avg_engagement = db.Column(db.Float, default=0.0) 