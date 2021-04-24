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


@app.route('/', methods=['GET', 'POST'])
def title():
    try:
        ava = current_user.photo
    except:
        ava = 'defold_avatarka.png'
    form = SearchForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        questions = db_sess.query(Questions).all()
        users = db_sess.query(User).all()
        questions.sort(key=lambda elem: elem.popular, reverse=True)
        questions = [(qst, user) for qst in questions
                     for user in users if user.id == qst.author]
        questions = [(qst, user, url_for('static', filename='img/avatars/' + user.photo), str(qst.date)[:16])
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
                               ava=url_for('static', filename='img/avatars/' + ava)
                               )


    else:
        qes = requests.get(f'http://localhost:8080/api/search/{form.search_line.data}').json()
        qes_id = list(map(lambda x: qes['qest'][x], qes['qest']))
        db_sess = db_session.create_session()
        questions = db_sess.query(Questions).all()
        users = db_sess.query(User).all()
        questions.sort(key=lambda elem: elem.popular, reverse=True)
        questions = [(qst, user) for qst in questions
                     for user in users if user.id == qst.author]
        questions = [(qst, user, url_for('static', filename='img/avatars/' + user.photo), str(qst.date)[:16])
                     for qst, user in questions]
        fo = []
        for i in questions:
            if i[0].id in qes_id:
                fo.append(i)
        questions = fo
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
                               ava=url_for('static', filename='img/avatars/' + ava)
                               )


@app.route('/about_us')
def about_us():
    try:
        ava = current_user.photo
    except:
        ava = 'defold_avatarka.png'
    return render_template('about_us.html',
                           css_file=url_for('static', filename='css/title_20.css'),
                           logo_photo=url_for('static', filename='img/logo_.png'),
                           new_ask=url_for('static', filename='img/new_ask.png'),
                           our=url_for('static', filename='img/our.png'),
                           my_ask=url_for('static', filename='img/my_ask.png'),
                           fon=url_for('static', filename='img/fon.png'),
                           andrey=url_for('static', filename='img/Andrey_op.png'),
                           vadim=url_for('static', filename='img/Vadim_op.png'),
                           boar=url_for('static', filename='img/boar.png'),
                           vk=url_for('static', filename='img/vk.png'),
                           insta=url_for('static', filename='img/insta.png'),
                           face=url_for('static', filename='img/face.png'),
                           git_hub=url_for('static', filename='img/git_hub.png'),
                           youtube=url_for('static', filename='img/YouTube.png'),
                           ava=url_for('static', filename='img/avatars/' + ava)
                           )


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        ava = current_user.photo
    except Exception:
        ava = 'defold_avatarka.png'
    form = RegisterForm()
    param = {'css_file': url_for('static', filename='css/title_20.css'),
             'logo_photo': url_for('static', filename='img/logo_.png'),
             'vk': url_for('static', filename='img/vk.png'),
             'insta': url_for('static', filename='img/insta.png'),
             'face': url_for('static', filename='img/face.png'),
             'git_hub': url_for('static', filename='img/git_hub.png'),
             'youtube': url_for('static', filename='img/YouTube.png'),
             'form': form,
             'fon': url_for('static', filename='img/fon.png'),
             'ava': url_for('static', filename='img/avatars/' + ava)}
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', message="Пароли не совпадают", **param)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', **param,
                                   message="Такой пользователь уже есть")
        try:
            id_for_avatar = max([user.id for user in db_sess.query(User).all()]) + 1
        except:
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
    try:
        ava = current_user.photo
    except:
        ava = 'defold_avatarka.png'
    form = LoginForm()
    param = {'css_file': url_for('static', filename='css/title_20.css'),
             'logo_photo': url_for('static', filename='img/logo_.png'),
             'vk': url_for('static', filename='img/vk.png'),
             'insta': url_for('static', filename='img/insta.png'),
             'face': url_for('static', filename='img/face.png'),
             'git_hub': url_for('static', filename='img/git_hub.png'),
             'youtube': url_for('static', filename='img/YouTube.png'),
             'form': form,
             'fon': url_for('static', filename='img/fon.png'),
             'ava': url_for('static', filename='img/avatars/' + ava)}
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               **param)
    return render_template('login.html', **param)


@app.route('/new_ask', methods=['GET', 'POST'])
def new_ask():
    try:
        ava = current_user.photo
    except:
        ava = 'defold_avatarka.png'
    form = AskForm()
    param = {'css_file': url_for('static', filename='css/title_20.css'),
             'logo_photo': url_for('static', filename='img/logo_.png'),
             'vk': url_for('static', filename='img/vk.png'),
             'insta': url_for('static', filename='img/insta.png'),
             'face': url_for('static', filename='img/face.png'),
             'git_hub': url_for('static', filename='img/git_hub.png'),
             'youtube': url_for('static', filename='img/YouTube.png'),
             'form': form,
             'fon': url_for('static', filename='img/fon.png'),
             'ava': url_for('static', filename='img/avatars/' + ava)}
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        try:
            id_for_fon = max([user.id for user in db_sess.query(Questions).all()]) + 1
        except:
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
    return render_template('new_ask.html', **param)


@app.route('/my_ask')
def my_ask():
    try:
        ava = current_user.photo
    except:
        ava = 'defold_avatarka.png'
    db_ses = db_session.create_session()
    param = {'css_file': url_for('static', filename='css/title_20.css'),
             'star_on_o': url_for('static', filename='img/star_on.png'),
             'star_off_o': url_for('static', filename='img/star_off.png'),
             'logo_photo': url_for('static', filename='img/logo_.png'),
             'vk': url_for('static', filename='img/vk.png'),
             'insta': url_for('static', filename='img/insta.png'),
             'face': url_for('static', filename='img/face.png'),
             'git_hub': url_for('static', filename='img/git_hub.png'),
             'youtube': url_for('static', filename='img/YouTube.png'),
             'fon': url_for('static', filename='img/fon.png'),
             'ava': url_for('static', filename='img/avatars/' + ava)
             }
    ask = db_ses.query(Questions).all()
    ask_mi = []
    for i in ask:
        if i.author == current_user.id:
            ask_mi.append(i)
    return render_template('my_ask.html', **param, ask=ask_mi)


@app.route('/inf_ask/pers_account/<int:user_id>')
def pers_account(user_id):
    try:
        ava = current_user.photo
    except:
        ava = 'defold_avatarka.png'
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    questions = db_sess.query(Questions).filter(Questions.author == user.id)
    # inf = [(qst.title, qst.question) for qst in questions]
    params = {
        'css_file': url_for('static', filename='css/title_20.css'),
        'star_on_o': url_for('static', filename='img/star_on.png'),
        'star_off_o': url_for('static', filename='img/star_off.png'),
        'user': user,
        'questions': questions,
        'avatar': url_for('static', filename='img/avatars/' + user.photo),
        'logo_photo': url_for('static', filename='img/logo_.png'),
        'vk': url_for('static', filename='img/vk.png'),
        'insta': url_for('static', filename='img/insta.png'),
        'face': url_for('static', filename='img/face.png'),
        'git_hub': url_for('static', filename='img/git_hub.png'),
        'youtube': url_for('static', filename='img/YouTube.png'),
        'fon': url_for('static', filename='img/fon.png'),
        'ava': url_for('static', filename='img/avatars/' + ava)
    }

    return render_template('profil.html', **params)


@app.route('/inf_ask/<int:qst_id>', methods=['GET', 'POST'])
def inf_ask(qst_id):
    try:
        ava = current_user.photo
    except:
        ava = 'defold_avatarka.png'
    form = CommForm()
    db_sess = db_session.create_session()
    ask = db_sess.query(Questions).filter(Questions.id == qst_id).first()
    param = {'css_file': url_for('static', filename='css/title_20.css'),
             'star_on_o': url_for('static', filename='img/star_on.png'),
             'star_off_o': url_for('static', filename='img/star_off.png'),
             'logo_photo': url_for('static', filename='img/logo_.png'),
             'vk': url_for('static', filename='img/vk.png'),
             'insta': url_for('static', filename='img/insta.png'),
             'face': url_for('static', filename='img/face.png'),
             'git_hub': url_for('static', filename='img/git_hub.png'),
             'youtube': url_for('static', filename='img/YouTube.png'),
             'ava': url_for('static', filename='img/avatars/' + ava),
             'fon': url_for('static', filename='img/fon.png')}

    if not ask:
        return render_template('error404.html')
    ask.popular += 1
    db_sess.commit()
    if form.validate_on_submit():
        text = form.comment.data
        comment = Comments(question_id=qst_id,
                           comment=text,
                           author=current_user.id, )
        db_sess.add(comment)
        db_sess.commit()
    param['fon_li'] = url_for('static', filename=f'img/avatars/{ask.photo}')
    comment = db_sess.query(Comments).filter(Comments.question_id == qst_id)
    comments = []
    for i in comment:
        user = db_sess.query(User).filter(User.id == i.author).first()
        comments.append([i.comment, user.name, user.surname, url_for('static', filename='img/avatars/' + user.photo)
                            , i.date, 'pers_account/' + str(i.author)])
    return render_template('read_ask.html', **param, ask=ask, commentar=comments, form=form)


@app.route('/delete/<int:id_quest>')
def del_quest(id_quest):
    try:
        ava = current_user.photo
    except:
        ava = 'defold_avatarka.png'
    db_sess = db_session.create_session()
    questions = db_sess.query(Questions).filter(Questions.id == id_quest).first()
    if current_user.id == questions.author:
        db_sess.delete(questions)
        db_sess.commit()
    return redirect('/my_ask')


@app.route('/qu_edit/<int:id>', methods=['GET', 'POST'])
def edit_qu(id):
    try:
        ava = current_user.photo
    except:
        ava = 'defold_avatarka.png'
    form = EditForm()
    param = {'css_file': url_for('static', filename='css/title_20.css'),
             'logo_photo': url_for('static', filename='img/logo_.png'),
             'vk': url_for('static', filename='img/vk.png'),
             'insta': url_for('static', filename='img/insta.png'),
             'face': url_for('static', filename='img/face.png'),
             'git_hub': url_for('static', filename='img/git_hub.png'),
             'youtube': url_for('static', filename='img/YouTube.png'),
             'form': form,
             'fon': url_for('static', filename='img/fon.png'),
             'ava': url_for('static', filename='img/avatars/' + ava)}
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
            return redirect('/my_ask')
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        questions = db_sess.query(Questions).filter(Questions.id == id).first()
        questions.title = form.title.data
        questions.question = form.question.data
        db_sess.commit()
        return redirect('/my_ask')
    return render_template('edit_ask.html', **param)


if __name__ == '__main__':
    db_session.global_init('db/posts.db')
    app.register_blueprint(search_api.blueprint)
    app.run(port=8080, host='127.0.0.1')
