import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Email, ValidationError, Length

from app.services import userService


class UsernamePasswordForm(FlaskForm):
    client_id = HiddenField()
    grant_type = HiddenField()
    username = StringField('Email', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=256)])


class UsernamePasswordResetForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])


class UsernamePasswordNewForm(FlaskForm):
    client_id = HiddenField()
    grant_type = HiddenField()
    reset_code = HiddenField()
    username = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=256)])
    password_repeat = PasswordField('Repeat Password', validators=[DataRequired()])


class AccountReactivateForm(FlaskForm):
    reactivation_code = HiddenField()
    username = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])


class SignupForm(FlaskForm):
    client_id = HiddenField()
    grant_type = HiddenField()
    alias = StringField('Alias', validators=[DataRequired(), Length(min=4, max=30)])
    username = StringField('Email', validators=[DataRequired(), Email(), Length(min=4, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=10, max=256)])
    password_repeat = PasswordField('Repeat Password', validators=[DataRequired()])

    """
    Validates the form by calling `validate` on each field, passing any
    extra `Form.validate_<fieldname>` validators to the field validator.
    """
    def validate_username(self, field):
        is_username_unique = userService.is_username_unique(field.data)

        if not is_username_unique:
            raise ValidationError('username is not unique')

    def validate_alias(self, field):
        pattern = r'[^\.A-Za-z0-9_]'
        if re.search(pattern, field.data):
            raise ValidationError('invalid characters for alias')

        is_alias_unique = userService.is_alias_unique(field.data)

        if not is_alias_unique:
            raise ValidationError('alias is not unique')

    def validate_password_repeat(self, field):

        if self.password.data != field.data:
            raise ValidationError('Passwords need to match')
