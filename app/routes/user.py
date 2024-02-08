import flask
import flask_login

from app.db import Session
from app.db.models import User

from . import bp


@flask_login.login_required
@bp.get("/me")
def me():
    return flask.redirect(
        flask.url_for(".user", slug=flask_login.current_user.slug)
    )


@bp.get("/users/<slug>")
def user(slug):
    with Session() as session:
        user = session.query(User).filter_by(slug=slug).first()
        if not user:
            by_name = session.query(User).filter_by(name=slug).first()
            if by_name:
                return flask.redirect(flask.url_for(".user", slug=by_name.slug))
            try:
                id = int(slug)
            except ValueError:
                flask.abort(404)
            user = session.query(User).filter_by(id=id).first()
        if not user:
            flask.abort(404)
        return flask.render_template("user.html", user=user)
