#!/bin/bash

python -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/alembic upgrade head
FLASK_DEBUG=1 ./.venv/bin/flask run
