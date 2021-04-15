from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class CommForm(FlaskForm):
    comment = StringField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Отправить')
