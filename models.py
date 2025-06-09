class LinkedInAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    access_token = db.Column(db.String(255))
    refresh_token = db.Column(db.String(255))
    profile_id = db.Column(db.String(255))
    profile_name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('linkedin_accounts', lazy=True))
    
    def __repr__(self):
        return f'<LinkedInAccount {self.email}>' 