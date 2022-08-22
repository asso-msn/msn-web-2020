from app import Blueprint


bp = Blueprint(__name__, name='main')


from . import auth, games, static_pages, user
from .api import bp as api
from .admin import bp as admin

bp.register_blueprint(api)
bp.register_blueprint(admin)
