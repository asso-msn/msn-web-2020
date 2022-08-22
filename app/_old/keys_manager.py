import logging
from pathlib import Path
import yaml

from app.models import Keys

class KeysManager:
    """
    Retrieves credentials
    """

    PATH = './keys.yaml'
    file_data = None

    @classmethod
    def _get_data(cls, key):
        if not cls.file_data:
            path = Path(cls.PATH)
            path.touch(exist_ok=True)
            cls.file_data = yaml.full_load(path.read_text())
        if not isinstance(cls.file_data, dict):
            logging.warning(f'Empty or invalid {cls.PATH}')
            cls.file_data = {}
        return cls.file_data.get(key) or Keys.query.filter_by(id=key).first()

    @classmethod
    def get(cls, key, *args, fallback=None):
        data = cls._get_data(key)
        for arg in args:
            data = data.get(arg)
            if data is None:
                break
        return data or fallback
