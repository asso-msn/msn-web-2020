python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
.\venv\Scripts\flask db upgrade
set FLASK_DEBUG=1
.\venv\Scripts\flask run