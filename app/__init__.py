from pathlib import Path

from flask_login import LoginManager

login_manager = LoginManager()
APP_DIR = Path(__file__)
APP_DIR = APP_DIR.parent.relative_to(APP_DIR.parent.parent)
CONFIG_PATH = Path("./config.yaml")


from app.application import App


@login_manager.user_loader
def load_user(id):
    from app.db import session
    from app.db.models import User

    return session.get(User, id)


app = App()

from app import db

app.after_request(db.after_request)

from app import templating

app.context_processor(templating.context_processor)
templating.register_filters(app)
