import flask

from . import bp


@bp.get("/")
def index():
    """Lists all routes"""
    routes = (
        {
            "func": flask.current_app.view_functions[x.endpoint],
            "rule": x,
        }
        for x in flask.current_app.url_map.iter_rules()
        if x.endpoint.startswith("main.admin")
    )
    return flask.render_template("admin/index.html", routes=routes)
