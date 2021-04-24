from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FileField, TextAreaField
from wtforms.validators import DataRequired


class EditForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    question = TextAreaField('Вопрос', validators=[DataRequired()])
    submit = SubmitField('Создать')
