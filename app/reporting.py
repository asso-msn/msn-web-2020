import logging
import sys
import requests

from .keys import Keys

def emit(msg: str, channel='log'):
    webhooks = Keys.get('webhooks')
    urls = webhooks.get(channel, webhooks.get('log', []))
    for url in urls:
        requests.post(url, json={'content': msg})

def log(*msgs, level=logging.INFO, sep='\n', out=sys.stderr):
    msg = sep.join(map(str, msgs))
    level_name = logging.getLevelName(level)
    print(f'[{level_name}] {msg}', file=out)
    out.flush()
    emit(msg)