from flask import url_for, redirect, render_template

from app.models import Staff
from .. import bp

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/welcome')
def welcome():
    return render_template('welcome.html')

@bp.route('/about-msn')
def about_msn():
    members = Staff.query.all()
    members = [members[0] for _ in range(10)]
    return render_template('about-msn.html', members=members)
