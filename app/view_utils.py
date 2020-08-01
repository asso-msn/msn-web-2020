from functools import wraps
from flask import flash, g, redirect

def form_route(route, app, form_class, *args, **kwargs):
    def decorator(func):
        kwargs['methods'] = kwargs.get('methods', ['GET', 'POST'])
        @app.route(route, *args, **kwargs)
        @wraps(func)
        def partial(*args, **kwargs):
            return func(form_class(), *args, **kwargs)
        return partial
    return decorator
