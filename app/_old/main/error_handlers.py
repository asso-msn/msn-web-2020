from flask import current_app

from app.exceptions import APIError
from . import bp

@bp.app_errorhandler(Exception)
def error_handler(e: Exception, code=500):
    if False and current_app.debug:
        raise e
    return str(e), code

@bp.app_errorhandler(APIError)
def apierror_handler(e: APIError):
    return error_handler(e, e.code)
