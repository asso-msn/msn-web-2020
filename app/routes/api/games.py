import flask

from . import bp
from app import permissions
from app.db import session
from app.db.models import Game


def remove_link(discord_role_id):
    game = session.query(Game).filter_by(discord_role_id=discord_role_id).first()
    if not game:
        return
    game.discord_role_id = None


def add_link(discord_role_id, name):
    game = session.query(Game).filter_by(name=name).first()
    if not game:
        game = Game()
        game.name = name
        session.add(game)
    game.discord_role_id = discord_role_id

@bp.post('/roles')
@permissions.admin_required
def update_link():
    """
    Links or unlinks Discord roles with games in db

    :param discord_role_id: Role to link to a game
    :param name: (Optional) Name to assign to the created game
    :param delete: (Optional) Boolean to indicate the remove the Discord role from db
    """
    id = flask.request.json['discord_role_id']
    if flask.request.json.get('delete'):
        remove_link(id)
    else:
        add_link(id, flask.request.json['name'])
    session.commit()
    return '', 200


@bp.post('/games/<slug>')
@permissions.admin_required
def update_game(slug):
    game = session.query(Game).filter_by(slug=slug).first()
    if not game:
        flask.abort(404)
    game.name = flask.request.json['name']
    game.slug = flask.request.json['slug']
    session.commit()
    return '', 200
