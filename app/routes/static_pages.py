import flask
from . import bp


@bp.get('/')
def index():
    return flask.render_template('index.html')
