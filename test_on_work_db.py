from data import db_session
from data.users import User
from data.questions import Questions
from data.comments import Comments


def add_user():
    db_sess = db_session.create_session()
    user = User(
        surname='Гулиев',
        name='Павел',
        email='1234567@yandex.ru'
    )
    user.set_password('qwerty')
    db_sess.add(user)
    db_sess.commit()


def add_question():
    db_sess = db_session.create_session()
    with open('main.txt') as file:
        text = file.read()
    question = Questions(
        author=3,
        title='Синтаксис python',
        question=text,
        popular=5
    )
    db_sess.add(question)
    db_sess.commit()


def add_comment():
    db_sess = db_session.create_session()
    comment = Comments(
        question_id=1,
        comment='Не знаю, нужно покапаться в инете',
    )
    db_sess.add(comment)
    db_sess.commit()


if __name__ == '__main__':
    db_session.global_init('db/posts.db')
    add_question()

