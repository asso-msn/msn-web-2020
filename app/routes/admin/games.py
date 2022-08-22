import flask

from . import bp
from app.db import session
from app.db.models import Game
from app.discord import bot


@bp.get('/roles')
def roles():
    """Manages bridges between games in db and Discord roles"""

    roles = bot.get_roles()
    for role in roles:
        db_role = session.query(Game).filter_by(discord_role_id=role['id']).first()
        role['db'] = db_role
    return flask.render_template('admin/roles.html', roles=roles)


@bp.get('/games')
def games():
    """Lists and allow for quick editing of games"""

    games = session.query(Game).all()
    games.sort(key=lambda x: x.slug)
    return flask.render_template('admin/games.html', games=games)


@bp.get('/games/<slug>')
def game_editor(slug):
    """Game entry editor"""

    game = session.query(Game).filter_by(slug=slug).first()
    if not game:
        flask.abort(404)
    return flask.render_template('admin/game_editor.html', game=game)
