import typing as t
import flask
import sqlalchemy as sa
from sqlalchemy import orm, MetaData
from werkzeug.local import LocalProxy

from app.config import Config
from .base import Base as CustomBase


meta = MetaData(naming_convention={
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
})

Base: t.Type[CustomBase] = orm.declarative_base(cls=CustomBase, metadata=meta)
engine = sa.create_engine(Config.DB_URL)
Session = orm.sessionmaker(bind=engine)


def get_session():
    if not 'session' in flask.g:
        print('Created session')
        flask.g.session = Session()
    return flask.g.session


session: orm.Session = LocalProxy(get_session)


def after_request(response):
    if 'session' in flask.g:
        flask.g.session.close()
        del flask.g.session
    return response
