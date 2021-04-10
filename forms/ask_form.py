from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, StringField, FileField
from wtforms.validators import DataRequired


class AskForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    question = StringField('Вопрос', validators=[DataRequired()])
    fon_photo = FileField('Загрузить фон', default='fon.jpg')
    submit = SubmitField('Создать')
