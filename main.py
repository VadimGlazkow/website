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
                               css_file=url_for('static', filename='css/title_20.css'),
                               questions=questions,
                               star_on_o=url_for('static', filename='img/star_on.png'),
                               star_off_o=url_for('static', filename='img/star_off.png'),
                               logo_photo=url_for('static', filename='img/logo_.png'),
                               new_ask=url_for('static', filename='img/new_ask.png'),
                               our=url_for('static', filename='img/our.png'),
                               my_ask=url_for('static', filename='img/my_ask.png'),
                               fon=url_for('static', filename='img/fon.png'),
                               vk=url_for('static', filename='img/vk.png'),
                               insta=url_for('static', filename='img/insta.png'),
                               face=url_for('static', filename='img/face.png'),
                               git_hub=url_for('static', filename='img/git_hub.png'),
                               youtube=url_for('static', filename='img/YouTube.png'),
                               )
    else:
        pass


@app.route('/about_us')
def about_us():
    return render_template('about_us.html',
                           css_file=url_for('static', filename='css/title_14.css'),
                           logo_photo=url_for('static', filename='img/logo_.png'),
                           new_ask=url_for('static', filename='img/new_ask.png'),
                           our=url_for('static', filename='img/our.png'),
                           my_ask=url_for('static', filename='img/my_ask.png'),
                           fon_my=url_for('static', filename='img/fon_my.png'),
                           andrey=url_for('static', filename='img/Andrey_op.png'),
                           vadim=url_for('static', filename='img/Vadim_op.png'),
                           boar=url_for('static', filename='img/boar.png'),
                           vk=url_for('static', filename='img/vk.png'),
                           insta=url_for('static', filename='img/insta.png'),
                           face=url_for('static', filename='img/face.png'),
                           git_hub=url_for('static', filename='img/git_hub.png'),
                           youtube=url_for('static', filename='img/YouTube.png'),
                           )


if __name__ == '__main__':
    db_session.global_init('db/posts.db')
    app.run(port=8080, host='127.0.0.1')