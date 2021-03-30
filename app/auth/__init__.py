from app import init_blueprint, login

bp = init_blueprint(__name__)

from . import routes

login.login_view = 'main.login'
