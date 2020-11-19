from flask import url_for, redirect, render_template

from . import bp

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/about-msn')
def about_msn():
    return render_templatr('about-msn.html')
