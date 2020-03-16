import functools

from flask import g, request

import orm

from dbconfig import get_session


def use_sql_session(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        g.session = get_session()

        res = f(*args, **kwargs)

        g.session.commit()

        return res

    return wrapper


def authentication_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get('X-Auth-Token')

        if token is None:
            raise Exception('X-Auth-Token header is missing')

        g.token = g.session.query(orm.Token).filter(orm.Token.id == token).one_or_none()

        if g.token is None:
            raise Exception('Token is invalid')

        g.user = g.token.user

        return f(*args, **kwargs)

    return wrapper