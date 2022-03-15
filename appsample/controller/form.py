from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField, BooleanField
from wtforms.validators import DataRequired, URL


class LoginForm(FlaskForm):
    account = StringField('帳號', validators=[DataRequired(message='Not Null')])
    password = PasswordField('密碼', validators=[DataRequired(message='Not Null')])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('登入')


class ModifyForm(FlaskForm):
    mid = HiddenField("mid")
    name = StringField('名稱', validators=[DataRequired(message='Not Null')])
    author = StringField('作者', validators=[DataRequired(message='Not Null')])
    group = StringField('群組')
    url = StringField('url', validators=[URL()])
    pages = StringField('頁數')
    submit = SubmitField('送出')
