from flask import Flask, render_template, url_for
from data import db_session
from data.users import User
from data.questions import Questions
from data.comments import Comments
from forms.search_form import SearchForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'


@app.route('/', methods=['GET', 'POST'])
def title():
    form = SearchForm()
    if form.validate_on_submit():
        return form.search_line.data
    return render_template('search.html', form=form,
                           css_file=url_for('static', filename='css/style.css'),
                           logo_photo=url_for('static', filename='img/Logo_web.png'),
                           new_ask=url_for('static', filename='img/new_ask.png'),
                           our=url_for('static', filename='img/our.png'),
                           my_ask=url_for('static', filename='img/my_ask.png'),
                           fon=url_for('static', filename='img/fon.png')
                           )


if __name__ == '__main__':
    # db_session.global_init('db/posts.db')
    app.run(port=8080, host='127.0.0.1')