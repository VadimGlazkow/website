from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# TextAreaField - нужно будет при добавлении вопроса


class SearchForm(FlaskForm):
    search_line = StringField()
    submit = SubmitField('Найти')
