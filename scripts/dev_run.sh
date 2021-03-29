#!/bin/bash

python -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/flask db upgrade
FLASK_DEBUG=1 ./.venv/bin/flask run
