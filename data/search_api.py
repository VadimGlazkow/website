import flask

from . import db_session
from .questions import Questions

blueprint = flask.Blueprint(
    'search_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/search/<ser>')
def get_news(ser):
    db_sess = db_session.create_session()
    qes = db_sess.query(Questions).all()
    if qes:
        id_list = {}
        n = 0
        for i in qes:
            if ser in i.title:
                id_list[n] = i.id
                n += 1
        return flask.jsonify(
        {
            'qest':id_list
        }
    )