from app import init_blueprint

bp = init_blueprint(__name__)

from . import filters, routes
