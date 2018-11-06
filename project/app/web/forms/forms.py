from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, ValidationError, Length

from project.app.services import userService

class UsernamePasswordForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=256)])

class SignupForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=10, max=256)])
    passwordRepeat = PasswordField('Repeat Password', validators=[DataRequired()])

    """
    Validates the form by calling `validate` on each field, passing any
    extra `Form.validate_<fieldname>` validators to the field validator.
    """
    def validate_username(self, field):
        print("validate_username->field.data=" + str(field.data))
        isUsernameUnique = userService.isUsernameUnique(field.data)

        if not isUsernameUnique:
            raise ValidationError('username is not unique')

    def validate_passwordRepeat(self, field):
        print("validate_passwordRepeat->field.data=" + str(field.data))
        print("validate_passwordRepeat->self.password=" + str(self.password.data))

        if self.password.data != field.data:
            raise ValidationError('Passwords need to match')

