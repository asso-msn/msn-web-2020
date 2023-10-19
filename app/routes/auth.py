import flask
import flask_login

from app import discord

from . import bp

LOOPBACK_ADDR = "http://127.0.0.1"


def get_callback_url():
    url = flask.url_for(".discord_callback", _external=True)
    if url.startswith(LOOPBACK_ADDR):
        print("Rewriting URL to localhost")
        url = "http://localhost" + url[len(LOOPBACK_ADDR) :]
    return url


@bp.get("/login")
def login():
    return flask.render_template("login.html")


@flask_login.login_required
@bp.get("/logout")
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for(".index"))


@bp.get("/login/discord")
def discord_login():
    callback = get_callback_url()
    url = discord.get_login_url(callback)
    return flask.redirect(url)


@bp.get("/login/discord/callback")
def discord_callback():
    callback = get_callback_url()
    try:
        discord.login(callback, flask.request.args.get("code"))
    except Exception as e:
        if flask.current_app.debug:
            raise e
        flask.flash("Could not authenticate with Discord")
        return flask.redirect(flask.url_for(".login"))
    return flask.redirect(flask.url_for(".index"))
