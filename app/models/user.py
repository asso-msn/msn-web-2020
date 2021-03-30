from functools import wraps
from flask_login import UserMixin, current_user, login_required
from flask import redirect
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True)
    _name = db.Column('name', db.String(64))
    password = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False)
    is_hidden = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<{0} #{1.id} {1.username}>'.format(type(self).__name, self)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return (
            self.password is not None and
            check_password_hash(self.password, password)
        )

    @property
    def name(self):
        return self._name or self.login

    @staticmethod
    def admin_required(func):
        @wraps(func)
        @login_required
        def partial(*args, **kwargs):
            if not current_user.is_admin:
                return 'User must be admin', 403
            return func(*args, **kwargs)
        return partial

    # @classmethod
    # @login.user_loader
    # def load_user(cls, id):
    #     return cls.query.get(int(id))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
