import random
from flask import current_app

from . import bp

@bp.add_app_template_filter
def refresh(x: str, debug_only=True):
    if debug_only and not current_app.debug:
        return x
    return f'{x}?{random.randint(1000, 9999)}'
