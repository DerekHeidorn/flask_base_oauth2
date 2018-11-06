from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, ValidationError

class UsernamePasswordForm(Form):
    username = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    """
    Validates the form by calling `validate` on each field, passing any
    extra `Form.validate_<fieldname>` validators to the field validator.
    """
    def validate_username(self, field):
        if len(field.data) > 2:
            raise ValidationError('Name must be less than 2 characters')

class SignupForm(Form):
    username = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    passwordRepeat = PasswordField('Repeat Password', validators=[DataRequired()])