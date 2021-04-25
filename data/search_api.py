import flask
from functools import lru_cache

from . import db_session
from .questions import Questions

blueprint = flask.Blueprint(
    'search_api',
    __name__,
    template_folder='templates'
)


def my_dist_cached(a, b):
    @lru_cache(maxsize=len(a) * len(b))
    def recursive(i, j):
        if i == 0 or j == 0:
            return max(i, j)
        elif a[i - 1] == b[j - 1]:
            return recursive(i - 1, j - 1)
        else:
            return 1 + min(
                recursive(i, j - 1),
                recursive(i - 1, j),
                recursive(i - 1, j - 1)
            )
    return recursive(len(a), len(b))


@blueprint.route('/api/search/<ser>')
def get_news(ser):
    db_sess = db_session.create_session()
    qes = db_sess.query(Questions).all()
    if qes:
        lst = []
        for i in qes:
            lev = my_dist_cached(ser.lower(), i.title.lower())
            bigger = max([len(ser), len(i.title)])
            pct = ((bigger - lev) / bigger) * 100
            if ser.lower() in i.title.lower():
                pct += 20
            if pct > 30:
                lst.append([i.id, pct])
        dit = {}
        lst.sort(key=lambda x: x[1], reverse=True)
        for num, (value, _) in enumerate(lst):
            dit[num] = value
        return flask.jsonify(
        {
            'qest': dit
        }
    )