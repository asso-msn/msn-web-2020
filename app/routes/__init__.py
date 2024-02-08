from app import Blueprint

bp = Blueprint(__name__, name="main")


from . import auth, games, static_pages, user
from .admin import bp as admin
from .api import bp as api

bp.register_blueprint(api)
bp.register_blueprint(admin)
