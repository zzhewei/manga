from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, URL


class ModifyForm(FlaskForm):
    mid = HiddenField("mid")
    name = StringField('名稱', validators=[DataRequired(message='Not Null')])
    author = StringField('作者', validators=[DataRequired(message='Not Null')])
    group = StringField('群組')
    url = StringField('url', validators=[URL()])
    pages = StringField('頁數')
    submit = SubmitField('送出')
    cancel = SubmitField('取消')
