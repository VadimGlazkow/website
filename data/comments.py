import sqlalchemy
from sqlalchemy import orm

from datetime import datetime
from .db_session import SqlAlchemyBase


class Comments(SqlAlchemyBase):
    __tablename__ = 'comments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    author = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey('users.id'))
    question_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey('questions.id'))
    comment = sqlalchemy.Column(sqlalchemy.Text)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    # popular = sqlalchemy.Column(sqlalchemy.Integer)

    question = orm.relation('Questions')
