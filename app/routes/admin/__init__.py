import flask

from app import Blueprint

bp = Blueprint(__name__, prefix=True)


from app import permissions


@bp.before_request
@permissions.admin_required
def permissions_requirement():
    pass


from . import games, index
