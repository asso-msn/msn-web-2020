from . import bp

@bp.route('test')
def test():
    return 'test succ'
