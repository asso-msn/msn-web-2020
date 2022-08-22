import json


def context_processor():
    return {
    }


def register_filters(app):
    @app.template_filter()
    def boolify(x):
        return 'true' if bool(x) else 'false'

    @app.template_filter()
    def checkify(x):
        return 'checked' if bool(x) else ''

    @app.template_filter()
    def dumps(x):
        return json.dumps(x, indent=2, default=str)

    @app.template_filter()
    def statusify(x):
        if bool(x):
            return '<span class="status ok">OK</span>'
        return '<span class="status fail">FAIL</span>'
