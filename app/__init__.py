import importlib
import os
from flask import Blueprint, Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config

db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()

def init_blueprint(module, prefix=False, **kwargs):
    name = module[len(__name__) + 1:]
    if prefix:
        kwargs['url_prefix'] = '/' + module.split('.')[-1]
    return Blueprint(name, module,
        static_folder='static',
        template_folder='templates',
        **kwargs,
    )

def create_app(config_path='polyrhythm.cfg'):
    os.environ['CONFIG_FILE'] = os.environ.get('CONFIG_FILE', config_path)
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.from_envvar('CONFIG_FILE', True)
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    for module in ['admin', 'auth', 'main']:
        module = importlib.import_module('{}.{}'.format(__name__, module))
        app.register_blueprint(module.bp)

    return app
