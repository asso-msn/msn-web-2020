from flask import render_template, request

from app import templating
from app.models import User

from . import bp

@bp.route('/')
def index():
    return 'test succ'

@bp.route('/users/')
def users():
    query = User.query
    return render_template(
        'admin_list.html', items=query.all(), fields=User.__table__.columns.keys(),
    )

@bp.route('/users/<int:id>')
def user(id):
    user = User.query.get(id)
    return render_template(
        'admin_item.html', inputs=templating.get_inputs(
            user,
            fields=['login', '_name', '_avatar_url', 'is_admin', 'is_hidden', 'socials']
        )
    )

@bp.route('/users/<int:id>', methods=['POST'])
def edit_user(id):
    user = User.query.get(id)
    return str(dict(request.form))
