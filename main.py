from flask import Flask
from data import db_session
from data.users import User
from data.questions import Questions
from data.comments import Comments

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'


@app.route('/')
def title():
    pass


if __name__ == '__main__':
    # db_session.global_init('db/posts.db')
    app.run(port=8080, host='127.0.0.1')