from app import db

class DiscordAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    access_token = db.Column(db.String)
    refresh_token = db.Column(db.String)
    user = db.relationship('User')
