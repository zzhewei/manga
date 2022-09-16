from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField, BooleanField, ValidationError, SelectField, TextAreaField
from wtforms.validators import DataRequired, URL, Length, Email, Regexp, EqualTo
from ..model import User
from flask_babel import lazy_gettext


class LoginForm(FlaskForm):
    account = StringField(lazy_gettext('Email/Account'), validators=[DataRequired(message='Not Null')])
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired(message='Not Null')])
    remember_me = BooleanField(lazy_gettext('Keep me logged in'))
    submit = SubmitField(lazy_gettext('Login'))


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    account = StringField(lazy_gettext('Account'), validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                                     lazy_gettext('Account must have only letters, numbers, dots or underscores'))])
    username = StringField(lazy_gettext('Username'), validators=[DataRequired()])
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired(), EqualTo('password2', message=lazy_gettext('Passwords must match.'))])
    password2 = PasswordField(lazy_gettext('Enter Password Again'), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('Register'))

    # in-line validator must start with validate_
    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError(lazy_gettext('Email already registered.'))

    def validate_account(self, field):
        if User.query.filter_by(account=field.data).first():
            raise ValidationError(lazy_gettext('Account already in use.'))


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


class ChangePermissionForm(FlaskForm):
    uid = HiddenField("uid")
    username = StringField(lazy_gettext('Username'), validators=[DataRequired()])
    userrole = SelectField(lazy_gettext('UserRole'), choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('Update'))
    delete = SubmitField(lazy_gettext('Delete'))


class SearchForm(FlaskForm):
    search = StringField('Search', render_kw={"placeholder": lazy_gettext('Enter Username..')})
    submit = SubmitField(lazy_gettext('Search'))


class AboutMeForm(FlaskForm):
    about_content = TextAreaField('about_content', render_kw={"placeholder": lazy_gettext('Enter Something..')})
    submit = SubmitField(lazy_gettext('Update'))


class UploadDeleteForm(FlaskForm):
    delete_mid = HiddenField("mid")
    delete = SubmitField(lazy_gettext('Delete'))


class ChangeSortForm(FlaskForm):
    sort_choice = SelectField("sort_choice", choices=[(1, lazy_gettext('Likes(Highest)')), (2, lazy_gettext('Likes(Lowest)')), (3, lazy_gettext('Date Modified(Newest)')),
                                                          (4, lazy_gettext('Date Modified(Oldest)')), (5, lazy_gettext('Date created(Newest)')), (6, lazy_gettext('Date created(Oldest)'))], coerce=int, validators=[DataRequired()])
