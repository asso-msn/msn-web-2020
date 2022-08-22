import os
import yaml

from app import CONFIG_PATH


def _get_bool(key, default=None, any=False):
    value = os.environ.get(key, default)
    if not value or any:
        return value is not None
    return value.lower() in ['1', 'yes', 'true', 'enable', 'enabled', 'on']


class Config:
    _parsed = False

    DB_URL = os.environ.get('DB_URI', 'sqlite:///./app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = _get_bool('DB_TRACK_MODIFICATIONS', any=True)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super cool secret key')

    DISCORD_CLIENT_ID = None
    DISCORD_PUBLIC_KEY = None
    DISCORD_CLIENT_SECRET = None

    @property
    @classmethod
    def SQLALCHEMY_DATABASE_URI(cls):
        return cls.DB_URL

    @classmethod
    def ensure_parse(cls):
        if cls._parsed or not CONFIG_PATH.exists():
            return
        with CONFIG_PATH.open() as f:
            config_data = yaml.safe_load(f)
            for key, value in config_data.items():
                setattr(Config, key, value)
        cls._parsed = True


Config.ensure_parse()
