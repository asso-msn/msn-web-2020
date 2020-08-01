from wtforms.validators import Length, ValidationError

from .main.models import User

def is_alnum_check(form, field):
    if not field.data.isalnum():
        raise ValidationError(
            'Please use only letters and numbers in your {}'.format(field.name)
        )

def length_validator(property):
    return Length(max=property.property.columns[0].type.length)

def username_taken_check(form, input):
    user = User.query.filter_by(name=input.data).first()
    if user is not None:
        raise ValidationError('This login is already taken')
