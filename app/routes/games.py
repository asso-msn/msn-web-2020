import flask

from app.db import session
from app.db.models import Game
from . import bp


@bp.get('/games')
def games():
    games = session.query(Game)
    return flask.render_template('games.html', games=games)
