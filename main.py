from flask import Flask, render_template, url_for, request, redirect
from flask_login import LoginManager, login_user, login_required,\
    logout_user, current_user
from data import db_session
from data.users import User
from data.questions import Questions
from data.comments import Comments
from forms.search_form import SearchForm
from forms.register_form import RegisterForm
from forms.login_form import LoginForm


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    param = {'css_file': url_for('static', filename='css/title_14.css'),
             'logo_photo': url_for('static', filename='img/logo_.png'),
             'vk': url_for('static', filename='img/vk.png'),
             'insta': url_for('static', filename='img/insta.png'),
             'face': url_for('static', filename='img/face.png'),
             'git_hub': url_for('static', filename='img/git_hub.png'),
             'youtube': url_for('static', filename='img/YouTube.png'),
             'form': form}
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', message="Пароли не совпадают", **param)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', **param,
                                   message="Такой пользователь уже есть")
        id_for_avatar = max([user.id for user in db_sess.query(User).all()]) + 1
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
    form = LoginForm()
    param = {'css_file': url_for('static', filename='css/title_14.css'),
             'logo_photo': url_for('static', filename='img/logo_.png'),
             'vk': url_for('static', filename='img/vk.png'),
             'insta': url_for('static', filename='img/insta.png'),
             'face': url_for('static', filename='img/face.png'),
             'git_hub': url_for('static', filename='img/git_hub.png'),
             'youtube': url_for('static', filename='img/YouTube.png'),
             'form': form}
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', **param)


if __name__ == '__main__':
    db_session.global_init('db/posts.db')
    app.run(port=8080, host='127.0.0.1')