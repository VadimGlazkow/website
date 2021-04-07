import sqlalchemy
from sqlalchemy import orm

from datetime import datetime
from .db_session import SqlAlchemyBase


class Questions(SqlAlchemyBase):
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    author = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey('users.id'))
    title = sqlalchemy.Column(sqlalchemy.String)
    question = sqlalchemy.Column(sqlalchemy.Text)
    popular = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)

    comment = orm.relation("Comments", back_populates='question')
    user = orm.relation('User')
