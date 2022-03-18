from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, URL, Length, Email, Regexp, EqualTo
from ..model import User


class LoginForm(FlaskForm):
    account = StringField('帳號', validators=[DataRequired(message='Not Null')])
    password = PasswordField('密碼', validators=[DataRequired(message='Not Null')])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('登入')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('帳號', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                   'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('密碼', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('再次輸入密碼', validators=[DataRequired()])
    submit = SubmitField('註冊')

    # in-line validator must start with validate_
    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Account already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ModifyForm(FlaskForm):
    mid = HiddenField("mid")
    name = StringField('名稱', validators=[DataRequired(message='Not Null')])
    author = StringField('作者', validators=[DataRequired(message='Not Null')])
    group = StringField('群組')
    url = StringField('url', validators=[URL()])
    pages = StringField('頁數')
    submit = SubmitField('送出')
