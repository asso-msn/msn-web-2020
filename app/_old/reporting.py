import logging
import sys
import requests

class WebhookHandler(logging.Handler):
    def emit(self, record):
        emit(self.format(record))


def emit(msg: str, channel='log'):
    from app.keys_manager import KeysManager
    webhooks = KeysManager.get('webhooks')
    urls = webhooks.get(channel, webhooks.get('log', []))
    for url in urls:
        requests.post(url, json={'content': msg})


def log(*msgs, level=logging.INFO, sep='\n', out=sys.stderr):
    msg = sep.join(map(str, msgs))
    level_name = logging.getLevelName(level)
    print(f'[{level_name}] {msg}', file=out)
    out.flush()
    if level >= logging.WARNING:
        emit(msg, channel='error')
    elif level >= logging.INFO:
        emit(msg)
