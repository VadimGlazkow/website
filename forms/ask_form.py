from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FileField, TextAreaField
from wtforms.validators import DataRequired


class AskForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    question = TextAreaField('Вопрос', validators=[DataRequired()])
    fon_photo = FileField('Загрузить фон', default='fon.jpg')
    submit = SubmitField('Создать')
