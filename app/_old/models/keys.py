from app import db

class Keys(db.Model):
    id = db.Column(db.String, primary_key=True)
    data = db.Column(db.JSON)
