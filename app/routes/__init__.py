from app import Blueprint


bp = Blueprint(__name__, name='front')


from . import auth, static_pages, user
