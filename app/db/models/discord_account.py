import sqlalchemy as sa
from sqlalchemy import orm

from app.db import Base


class DiscordAccount(Base):
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    access_token = sa.Column(sa.String)
    refresh_token = sa.Column(sa.String)
    avatar = sa.Column(sa.String)

    user = orm.relationship("User", back_populates="discord", uselist=False)

    def call(self, *args, **kwargs):
        from app import discord

        kwargs["token"] = self.access_token
        return discord.call(*args, **kwargs)

    def update_avatar(self, data=None):
        if data is None:
            resp = self.call("/users/@me")
            data = resp.json()
        user_id = data.get("id")
        avatar_hash = data.get("avatar")
        self.avatar = (
            f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png"
        )
