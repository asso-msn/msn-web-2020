import operator

from app.config import Config

from . import call as _call


def call(*args, **kwargs):
    kwargs["bot"] = Config.DISCORD_BOT_TOKEN
    return _call(*args, **kwargs).json()


def get_roles():
    roles = call(f"/guilds/{Config.DISCORD_SERVER_ID}/roles")
    roles.sort(key=operator.itemgetter("position"), reverse=True)
    return roles
