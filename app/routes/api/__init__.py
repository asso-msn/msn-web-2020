import traceback

from app import Blueprint


bp = Blueprint(__name__, prefix=True)


@bp.errorhandler(Exception)
def errorhandler(e: Exception):
    code = e.code if hasattr(e, 'code') else None
    traceback.print_exc()
    return {'code': code, 'msg': str(e)}, code or 500


from . import games
