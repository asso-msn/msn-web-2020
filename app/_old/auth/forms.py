from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Length, Email

from app.form_utils import length_validator, is_alnum_check, username_taken_check
from app.models import User

class LoginForm(FlaskForm):
    login = StringField('Nom d\'utilisateur', validators=[
        DataRequired(),
        is_alnum_check,
    ])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Rester connecté')
    submit = SubmitField('Me connecter')

class RegistrationForm(FlaskForm):
    login = StringField('Nom d\'utilisateur', validators=[
        DataRequired(),
        username_taken_check,
        is_alnum_check,
    ])
    name = StringField('Nom d\'affichage', validators=[length_validator(User._name)])
    password = LoginForm.password
    remember_me = LoginForm.remember_me
    submit = SubmitField('M\'inscire')
