from . import bp

@bp.route('/')
def index():
    return 'test succ'
