import flask_login
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext import hybrid

from app.db import Base


class User(Base, flask_login.UserMixin):
    id = sa.Column(sa.Integer, primary_key=True)
    slug = sa.Column(sa.String)
    _name = sa.Column("name", sa.String)
    email = sa.Column(sa.String)
    password_hash = sa.Column(sa.String)
    is_admin = sa.Column(sa.Boolean)

    discord = orm.relationship(
        "DiscordAccount", back_populates="user", uselist=False
    )

    @hybrid.hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self.set_slug("slug", value)
        self._name = value

    @property
    def avatar(self):
        if self.discord:
            return self.discord.avatar
        return None
