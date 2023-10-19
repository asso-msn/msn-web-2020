import importlib

import flask
import flask_assets

from app import config, login_manager


class Blueprint(flask.Blueprint):
    def __init__(self, module_name: str, prefix=False, name=None):
        # if name is not None:
        #     name  = name
        # else:
        #     name = module_name.replace('.', '_')
        name = name or module_name.split(".")[-1]
        if prefix == False:
            prefix = None
        elif prefix == True:
            prefix = "/" + module_name.split(".")[-1]
        super().__init__(name, module_name, url_prefix=prefix)


class App(flask.Flask):
    def __init__(self):
        super().__init__(__name__.split(".")[0])
        config.Config.ensure_parse()
        self.config.from_object(config.Config)
        # self.add_blueprints(self, 'modules')
        self.load_assets()

        login_manager.init_app(self)

        from app import cli, routes

        self.register_blueprint(cli.bp)
        self.register_blueprint(routes.bp)

    def load_assets(self):
        from app import APP_DIR

        self.assets = flask_assets.Environment(self)
        bundles_path = APP_DIR / "static" / "bundles"
        if not bundles_path.exists():
            return
        for path in bundles_path.glob("*/"):
            type = path.stem
            output = f"bundle.{type}"
            path = path.resolve()
            files = path.rglob(f"*.{type}")
            bundle = flask_assets.Bundle(
                *(str(x) for x in files),
                output=output,
            )
            self.assets.register(type, bundle)
            bundle.build()

    @staticmethod
    def add_blueprints(obj, path="."):
        from app import APP_DIR

        for path in (APP_DIR / path).glob("*"):
            if path.stem.startswith("_"):
                continue
            module = importlib.import_module(".".join(path.parts))
            if not hasattr(module, "bp"):
                continue
            obj.register_blueprint(module.bp)
