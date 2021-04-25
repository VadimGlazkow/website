from flask import Flask, render_template, url_for, request, redirect, abort
from flask_login import LoginManager, login_user, login_required, \
    logout_user, current_user
import requests
from data import db_session
from data.users import User
from data.questions import Questions
from data.comments import Comments
from forms.search_form import SearchForm
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from forms.ask_form import AskForm
from forms.edit_ask import EditForm
from forms.new_com_form import CommForm
from data import search_api
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def check_password(password):
    if len(password) < 8:
        return 'Длина пароля меньше 8 символов'
    if not [None for letter in password if letter in '0123456789']:
        return 'В пароле нет цифр'
    if not [None for letter in password if letter.islower()]:
        return 'Пароль не имеет букв нижнего регистра'
    if not [None for letter in password if letter.isupper()]:
        return 'Пароль не имеет букв верхнего регистра'


def check_email(email):
    lines = "1234567890-=;'\.|qwertyuiop[]asdfghjkl;'zxcvbnm,./"
    email = email.split('@')[0]
    if [None for letter in email if letter not in lines]:
        'В логине используюся буквы других алфавитов'


def stay_ava():
    if current_user.is_authenticated:
        return current_user.photo
    else:
        return 'defold_avatarka.png'


def return_files(ava=None, form=None, qst=None):
    return {'css_file': url_for('static', filename='css/title_20.css'),
            'star_on_o': url_for('static', filename='img/star_on.png'),
            'star_off_o': url_for('static', filename='img/star_off.png'),
            'logo_photo': url_for('static', filename='img/logo_.png'),
            'new_ask': url_for('static', filename='img/new_ask.png'),
            'our': url_for('static', filename='img/our.png'),
            'my_ask': url_for('static', filename='img/my_ask.png'),
            'fon': url_for('static', filename='img/fon.png'),
            'vk': url_for('static', filename='img/vk.png'),
            'insta': url_for('static', filename='img/insta.png'),
            'face': url_for('static', filename='img/face.png'),
            'git_hub': url_for('static', filename='img/git_hub.png'),
            'youtube': url_for('static', filename='img/YouTube.png'),
            'ava': url_for('static', filename='img/avatars/' + ava),
            'form': form,
            'questions': qst}


@app.route('/', methods=['GET', 'POST'])
def title():
    ava = stay_ava()
    form = SearchForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        questions = db_sess.query(Questions).all()
        users = db_sess.query(User).all()
        questions.sort(key=lambda elem: elem.popular, reverse=True)
        questions = [(qst, user) for qst in questions
                     for user in users if user.id == qst.author]
        questions = [(qst, user, url_for('static', filename='img/avatars/' + user.photo),
                      str(qst.date)[:16])
                     for qst, user in questions]
        params = return_files(ava=ava, form=form, qst=questions)
        return render_template('search.html', **params)
    else:
        qes = requests.get(f'http://localhost:8080/api/search/{form.search_line.data}').json()
        qes_id = list(map(lambda x: qes['qest'][x], qes['qest']))
        db_sess = db_session.create_session()
        questions = db_sess.query(Questions).all()
        users = db_sess.query(User).all()
        questions.sort(key=lambda elem: elem.popular, reverse=True)
        questions = [(qst, user) for qst in questions
                     for user in users if user.id == qst.author]
        questions = [(qst, user, url_for('static', filename='img/avatars/' + user.photo),
                      str(qst.date)[:16]) for qst, user in questions]
        fo = []
        for i in questions:
            if i[0].id in qes_id:
                fo.append(i)
        questions = fo
        params = return_files(ava=ava, form=form, qst=questions)
        return render_template('search.html', **params)


@app.route('/about_us')
def about_us():
    ava = stay_ava()
    params = return_files(ava=ava)
    return render_template('about_us.html', **params)


@app.route('/register', methods=['GET', 'POST'])
def register():
    ava = stay_ava()
    form = RegisterForm()
    param = return_files(ava=ava, form=form)
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', message="Пароли не совпадают", **param)
        check_pass = check_password(form.password.data)
        if check_pass:
            return render_template('register.html', **param,
                                   message=check_pass)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', **param,
                                   message="Такой пользователь уже есть")
        if check_email(form.email.data):
            return render_template('register.html', **param,
                                   message=check_email(form.email.data))
        try:
            id_for_avatar = max([user.id for user in db_sess.query(User).all()]) + 1
        except ValueError:
            id_for_avatar = 0
        photo = form.avatar_photo.data
        if photo:
            with open(f'static/img/avatars/{id_for_avatar}_avatar.png', 'wb') as file:
                file.write(photo.read())
            photo = f'{id_for_avatar}_avatar.png'
        else:
            photo = 'defold_avatarka.png'
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            photo=photo
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('register.html', **param)


@app.route('/login', methods=['GET', 'POST'])
def login():
    ava = stay_ava()
    form = LoginForm()
    params = return_files(ava=ava, form=form)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               **params)
    return render_template('login.html', **params)


@app.route('/new_ask', methods=['GET', 'POST'])
def new_ask():
    ava = stay_ava()
    form = AskForm()
    params = return_files(ava=ava, form=form)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        try:
            id_for_fon = max([user.id for user in db_sess.query(Questions).all()]) + 1
        except ValueError:
            id_for_fon = 0
        fon = form.fon_photo.data
        if fon:
            with open(f'static/img/avatars/{id_for_fon}_fon.png', 'wb') as file:
                file.write(fon.read())
            photo = f'{id_for_fon}_fon.png'
        else:
            photo = 'fon.png'
        qust = Questions(
            author=current_user.id,
            title=form.title.data,
            question=form.question.data,
            photo=photo
        )
        db_sess.add(qust)
        db_sess.commit()
        return redirect('/')
    return render_template('new_ask.html', **params)


@app.route('/my_ask')
def my_ask():
    ava = stay_ava()
    db_ses = db_session.create_session()
    param = return_files(ava=ava)
    ask = db_ses.query(Questions).all()
    ask_mi = []
    for i in ask:
        if i.author == current_user.id:
            ask_mi.append(i)
    return render_template('my_ask.html', **param, ask=ask_mi)


@app.route('/inf_ask/pers_account/<int:user_id>')
def pers_account(user_id):
    ava = stay_ava()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    questions = db_sess.query(Questions).filter(Questions.author == user.id)
    params = {**return_files(ava=ava, qst=questions),
              **{'avatar': url_for('static', filename='img/avatars/' + user.photo),
                 'user': user}}
    return render_template('profil.html', **params)


@app.route('/inf_ask/<int:qst_id>', methods=['GET', 'POST'])
def inf_ask(qst_id):
    form = CommForm()
    db_sess = db_session.create_session()
    ask = db_sess.query(Questions).filter(Questions.id == qst_id).first()
    if not ask:
        return render_template('error404.html')
    user = db_sess.query(User).filter(User.id == ask.author).first()
    param = return_files(form=form, ava=user.photo)
    ask.popular += 1
    db_sess.commit()
    if form.validate_on_submit():
        text = form.comment.data
        comment = Comments(question_id=qst_id,
                           comment=text,
                           author=current_user.id)
        db_sess.add(comment)
        db_sess.commit()
    param['stay_photo'] = 1
    if ask.photo in ('fon.png', '0_fon.png'):
        param['stay_photo'] = 0
    else:
        param['fon_li'] = url_for('static', filename=f'img/avatars/{ask.photo}')
    comment = db_sess.query(Comments).filter(Comments.question_id == qst_id)
    comments = []
    for i in comment:
        user = db_sess.query(User).filter(User.id == i.author).first()
        comments.append([i.id, i.color, i.comment, user.name, user.surname,
                         url_for('static', filename='img/avatars/' + user.photo),
                         i.date, 'pers_account/' + str(i.author)])

    return render_template('read_ask.html', **param, ask=ask,
                           commentar=comments)


@app.route('/delete_ask/<int:id_quest>/<redirct>')
def del_quest(id_quest, redirct):
    db_sess = db_session.create_session()
    questions = db_sess.query(Questions).filter(Questions.id == id_quest).first()
    os.remove(f'static/img/avatars/{questions.id}_fon.png')
    if current_user.id == questions.author:
        db_sess.delete(questions)
        db_sess.commit()
    if redirct == 'title':
        redirct = '/'
    else:
        redirct = '/my_ask'
    return redirect(redirct)


@app.route('/qu_edit/<int:id>/<redirct>', methods=['GET', 'POST'])
def edit_qu(id, redirct):
    if redirct == 'inf_ask':
        redirct += f'/{id}'
    ava = stay_ava()
    form = EditForm()
    param = return_files(ava=ava, form=form)
    if request.method == "GET":
        db_sess = db_session.create_session()
        questions = db_sess.query(Questions).filter(Questions.id == id).first()
        if questions.author == current_user.id:
            if questions:
                form.title.data = questions.title
                form.question.data = questions.question
            else:
                abort(404)
        else:
            return redirect(f'/{redirct}')
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        questions = db_sess.query(Questions).filter(Questions.id == id).first()
        questions.title = form.title.data
        questions.question = form.question.data
        db_sess.commit()
        return redirect(f'/{redirct}')
    return render_template('edit_ask.html', **param)


@app.route('/close_ask/<int:id_quest>/<redirct>')
def close_ask(id_quest, redirct):
    db_sess = db_session.create_session()
    questions = db_sess.query(Questions).filter(Questions.id == id_quest).first()
    if current_user.id == questions.author:
        questions.activity = abs(questions.activity - 1)
        db_sess.commit()
    if redirct == 'inf_ask':
        redirct += f'/{id_quest}'
    return redirect(f'/{redirct}')


@app.route('/color_com/<int:id>')
def color_ask(id):
    db_sess = db_session.create_session()
    comment = db_sess.query(Comments).filter(Comments.id == id).first()
    qst = db_sess.query(Questions).filter(Questions.id == comment.question_id).first()
    if current_user.id == qst.author:
        comment.color = abs(comment.color - 1)
        db_sess.commit()
    return redirect(f'/inf_ask/{qst.id}')


if __name__ == '__main__':
    db_session.global_init('db/posts.db')
    app.register_blueprint(search_api.blueprint)
    app.run(port=8080, host='127.0.0.1')
