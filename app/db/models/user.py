import flask_login
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext import hybrid

from app.db import Base, Session


class User(Base, flask_login.UserMixin):
    id = sa.Column(sa.Integer, primary_key=True)
    slug = sa.Column(sa.String)
    _name = sa.Column('name', sa.String)
    email = sa.Column(sa.String)
    password_hash = sa.Column(sa.String)

    discord = orm.relationship('DiscordAccount', back_populates='user', uselist=False)

    @hybrid.hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        slug = value.lower().replace(' ', '-')
        with Session() as session:
            if session.query(type(self)).filter_by(slug=slug).first():
                raise Exception('Duplicate name')
        self.slug = slug
        self._name = value

    @property
    def avatar(self):
        if self.discord:
            return self.discord.avatar
        return None
