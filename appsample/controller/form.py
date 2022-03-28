from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, URL, Length, Email, Regexp, EqualTo
from ..model import User
from flask_babel import lazy_gettext


class LoginForm(FlaskForm):
    account = StringField(lazy_gettext('Account'), validators=[DataRequired(message='Not Null')])
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired(message='Not Null')])
    remember_me = BooleanField(lazy_gettext('Keep me logged in'))
    submit = SubmitField(lazy_gettext('Login'))


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField(lazy_gettext('Account'), validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                                      lazy_gettext('Usernames must have only letters, numbers, dots or underscores'))])
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired(), EqualTo('password2', message=lazy_gettext('Passwords must match.'))])
    password2 = PasswordField(lazy_gettext('Enter Password Again'), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('Register'))

    # in-line validator must start with validate_
    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError(lazy_gettext('Account already registered.'))

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(lazy_gettext('Username already in use.'))


class ModifyForm(FlaskForm):
    mid = HiddenField("mid")
    name = StringField(lazy_gettext('Name'), validators=[DataRequired(message='Not Null')])
    author = StringField(lazy_gettext('Author'), validators=[DataRequired(message='Not Null')])
    group = StringField(lazy_gettext('Group'))
    url = StringField('url', validators=[URL()])
    pages = StringField(lazy_gettext('Page'))
    submit = SubmitField(lazy_gettext('Send'))


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(lazy_gettext('Old password'), validators=[DataRequired()])
    password = PasswordField(lazy_gettext('New password'), validators=[DataRequired(), EqualTo('password2', message=lazy_gettext('Passwords must match.'))])
    password2 = PasswordField(lazy_gettext('Confirm new password'), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('Update'))
