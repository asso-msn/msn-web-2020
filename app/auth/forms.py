from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Length, Email

from ..main.models import User
from ..form_utils import length_validator, is_alnum_check, username_taken_check

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[
        DataRequired(),
        length_validator(User.name),
        is_alnum_check,
    ])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Rester connecté')
    submit = SubmitField('Me connecter')

class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[
        DataRequired(),
        length_validator(User.name),
        username_taken_check,
        is_alnum_check,
    ])
    password = LoginForm.password
    remember_me = LoginForm.remember_me
    submit = SubmitField('M\'inscire')

