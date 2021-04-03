from app import db

class Member(db.Model):
    """
    Represents a member of the MSN organization, as in someone who is a staff
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    full_name = db.Column(db.String)
    _alias = db.Column('alias', db.String)
    _role = db.Column('role', db.String)
    avatar_override = db.Column(db.String)

    @property
    def alias(self):
        return self._alias or self.user.name

    @property
    def role(self):
        return self._role or 'Staff'

    @property
    def avatar_url(self):
        return self.avatar_override or self.user.avatar_url
