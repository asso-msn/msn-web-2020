from wtforms.validators import Length, ValidationError

from app.models import User

def is_alnum_check(form, field):
    if not field.data.isalnum():
        raise ValidationError(
            'Please use only letters and numbers in your {}'.format(field.name)
        )

def length_validator(property):
    length = property.property.columns[0].type.length
    if not length:
        raise TypeError(f'Argument {property} does not have a length')
    return Length(max=length)

def username_taken_check(form, input):
    user = User.query.filter_by(login=input.data).first()
    if user is not None:
        raise ValidationError('This login is already taken')
