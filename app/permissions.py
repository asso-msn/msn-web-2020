import functools

import flask_login


def admin_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        print("decorated admin view")
        user = flask_login.current_user
        if not user.is_authenticated or not user.is_admin:
            print(flask_login.current_user)
            raise Exception("Unauthorized")
        return f(*args, **kwargs)

    return wrapper
