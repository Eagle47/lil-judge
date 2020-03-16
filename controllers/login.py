from flask import request, g

from decorators import use_sql_session, authentication_required
from app import app

from controllers import utils

import orm

import uuid


@app.route('/login/', methods=['POST'])
@use_sql_session
def login():
    r = request.get_json()
    user = utils.get_user(
        r['username'],
        r['password']
    )

    if user is None:
        return {
            'error': 'Access denied'
        }

    token_id = str(uuid.uuid4())
    g.session.add(orm.Token(
        id=token_id,
        user_id=user.id
    ))

    return {'token': token_id}


@app.route('/logout/', methods=['DELETE'])
@use_sql_session
@authentication_required
def logout():
    g.session.delete(g.token)

    return {}