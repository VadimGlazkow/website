from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchForm(FlaskForm):
    search_line = StringField()
    submit = SubmitField('Найти')
