from flask import url_for, redirect, render_template

from .. import bp

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/welcome')
def welcome():
    return render_template('welcome.html')

@bp.route('/about-msn')
def about_msn():
    return render_template('about-msn.html')
