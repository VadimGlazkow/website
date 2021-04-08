from flask import Flask, render_template, url_for, request
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
    if request.method == 'GET':
        db_sess = db_session.create_session()
        questions = db_sess.query(Questions).all()
        users = db_sess.query(User).all()
        questions.sort(key=lambda elem: elem.popular, reverse=True)
        questions = [(qst, user) for qst in questions
                     for user in users if user.id == qst.author]
        questions = [(qst, user, url_for('static', filename='img/' + user.photo), str(qst.date)[:16])
                     for qst, user in questions]
        return render_template('search.html', form=form,
                               css_file=url_for('static', filename='css/title_14.css'),
                               questions=questions,
                               star_on=url_for('static', filename='img/star_on.png'),
                               star_off=url_for('static', filename='img/star_off.png'))
    else:
        pass


if __name__ == '__main__':
    db_session.global_init('db/posts.db')
    app.run(port=8080, host='127.0.0.1')