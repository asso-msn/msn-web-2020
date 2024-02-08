import urllib.parse

import flask_login

from app.config import Config
from app.db import Session
from app.db.models import DiscordAccount, User

from . import API_ENDPOINT, call

AUTHORIZE_ROUTE = "oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&prompt=consent&scope={scope}"
SCOPES = [
    "identify",
    # 'email',
]


def get_auth_params(callback, full=False, urlencode=None):
    if urlencode is None:
        urlencode = not full
    if not Config.DISCORD_CLIENT_ID:
        raise Exception("Discord API credentials not found")
    if urlencode:
        urllib.parse.quote(callback, safe="")
    result = {
        "scope": "%20".join(SCOPES),
        "redirect_uri": callback,
        "client_id": Config.DISCORD_CLIENT_ID,
    }
    if full:
        result.update({"client_secret": Config.DISCORD_CLIENT_SECRET})
    return result


def auth_from_code(callback, code):
    data = get_auth_params(callback, full=True)
    data.update(
        {
            "grant_type": "authorization_code",
            "code": code,
        }
    )
    # !!! Not specifying the content type will reset the user's preferences !!!
    response = call("/oauth2/token", data=data, type="form")
    if not response.ok:
        raise Exception(
            f"Could not authorize user to Discord: {response} {response.content.decode()}"
        )
    return response.json()


def get_login_url(callback):
    """Creates the OAuth login URL for the application"""

    route = AUTHORIZE_ROUTE.format(**get_auth_params(callback))
    return f"{API_ENDPOINT}/{route}"


def login(callback, code, register=True):
    """Logins a user to Discord using the code passed to the callback URL"""

    result = auth_from_code(callback, code)
    access_token = result.get("access_token")
    response = call("/oauth2/@me", token=access_token)
    if not response.ok:
        raise Exception("Could not authorize to Discord")
    user_response = response.json()["user"]
    print("User fetched from Discord API", user_response)
    id = int(user_response["id"])
    with Session() as session:
        discord_account = session.get(DiscordAccount, id)
        if not discord_account:
            if not register:
                raise Exception("No matching Discord account")
            discord_account = DiscordAccount(id=id, access_token=access_token)
            user = User(discord=discord_account)
            user.discord.update_avatar(data=user_response)
            session.add(discord_account, user)
        discord_account.access_token = access_token
        discord_account.refresh_token = result.get("refresh_token")
        if not discord_account.user.name:
            discord_account.user.name = user_response["username"]
        session.commit()
        flask_login.login_user(discord_account.user, remember=True)
    return discord_account
