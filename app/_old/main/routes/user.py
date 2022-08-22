from flask import redirect, url_for
from flask_login import current_user, login_required

from app import db
from app.models import User
from .. import bp


@login_required
@bp.route('/me')
def me():
    return redirect(url_for('.user', id=current_user.id))

@login_required
@bp.route('/me/deactivate')
def deactivate():
    current_user.delete()
    db.session.commit()
    return redirect(url_for('.home'))

@bp.route('/user/<id>')
def user(id):
    user = User.query.get(id) or User.query.filter_by(login=id).first()
    if not user:
        return 'User not found', 404
    return str(user)
