import sqlalchemy as sa
from sqlalchemy.ext import hybrid

from app.db import Base


class Game(Base):
    id = sa.Column(sa.Integer, primary_key=True)
    slug = sa.Column(sa.String)
    discord_role_id = sa.Column(sa.Integer)
    _name = sa.Column("name", sa.String, nullable=False)

    @hybrid.hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self.set_slug("slug", value, replace=False)
        self._name = value
