from .. import init_blueprint
from ..main.models import User

bp = init_blueprint(__name__, prefix=True)

@bp.before_request
@User.admin_required
def before_request():
    ''' Protect all admin endpoints '''
    pass


from . import routes
