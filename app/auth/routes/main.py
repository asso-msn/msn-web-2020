from flask import flash, render_template, redirect, request, url_for
from flask_login import login_user
from werkzeug.urls import url_parse

from app import db
from app.models import DiscordAccount, User
from .. import bp
from ..forms import LoginForm, RegistrationForm

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    def render():
        return render_template('login.html', title='Se connecter', form=form)
    if not form.validate_on_submit():
        return render()
    user = User.query.filter_by(name=form.login.data).first()
    if user is None or not user.check_password(form.password.data):
        flash('Nom d\'utilisateur ou mot de passe incorrect')
        return render()
    login_user(user, remember=form.remember_me.data)
    usual_next = url_for('main.index')
    next_page = request.args.get('next', usual_next)
    if url_parse(next_page).netloc:
        flash('Abnormal redirect detected')
        next_page = usual_next
    return redirect(next_page)

@bp.route('/register', methods=['GET', 'POST'])
def register_post():
    form = RegistrationForm()
    if not form.validate_on_submit():
        return render_template('login.html', title='S\'inscire', form=form)
    user = User(login=form.login.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash(f'Bienvenue parmi nous, {user.name} !')
    login_user(user, remember=form.remember_me.data)
    return redirect(url_for('main.home'))

