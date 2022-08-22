from functools import wraps
from flask_login import UserMixin, current_user, login_required
from flask import url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login, logger
from app.exceptions import InsufficientPermissionsError

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True)
    _name = db.Column('name', db.String(64))
    _avatar_url = db.Column('avatar_url', db.String)
    password = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False)
    is_hidden = db.Column(db.Boolean, default=False)
    socials = db.Column(db.JSON)

    def __repr__(self):
        return f'<{self.__class__.__name__} #{self.id} {self.name}>'

    def __str__(self):
        return self.name

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

    @property
    def avatar_url(self):
        return self._avatar_url or 'https://osu.ppy.sh/images/layout/avatar-guest.png'

    @property
    def socials_html(self):
        from app import templating
        return templating.handle_socials(self.socials)

    @staticmethod
    def admin_required(func):
        @wraps(func)
        @login_required
        def partial(*args, **kwargs):
            if not current_user.is_admin:
                raise InsufficientPermissionsError
            return func(*args, **kwargs)
        return partial

    @property
    def link(self):
        return url_for('main.user', id=self.login or self.id)

    @property
    def discord(self):
        from app.models import DiscordAccount
        return DiscordAccount.query.filter_by(user_id=self.id).first()

    def delete(self):
        from app.models import DiscordAccount
        DiscordAccount.query.filter_by(user_id=self.id).delete()
        db.session.delete(self)

    def set_avatar_from_discord(self, data=None):
        if data is None:
            resp = self.discord.call('/users/@me')
            logger.debug('Discord resp', resp, resp.json())
            data = resp.json()
        user_id = data.get('id')
        avatar_hash = data.get('avatar')
        self._avatar_url = f'https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png'
        return self


    # @classmethod
    # @login.user_loader
    # def load_user(cls, id):
    #     return cls.query.get(int(id))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
