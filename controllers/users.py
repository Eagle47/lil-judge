from decorators import authentication_required, use_sql_session
from app import app
from orm import User, ContestMember, Token
from flask import g, request

from . import utils


def user2json(u):
    return {
        'id': u.id,
        'username': u.username,
        'first_name': u.first_name,
        'las_name': u.last_name,
        'is_admin': u.is_admin
    }


@app.route("/users/")
@use_sql_session
@authentication_required
def list_users():
    return {
        'users': [user2json(user) for user in g.session.query(User)]
    }


@app.route("/users/<id>/")
@use_sql_session
@authentication_required
def get_user(id):
    return user2json(
        g.session.query(User).filter(User.id == id).one()
    )


@app.route("/users/<id>/", methods=['DELETE'])
@use_sql_session
@authentication_required
def delete_user(id):
    g.session.query(ContestMember).filter(ContestMember.user_id == id).delete()
    g.session.query(Token).filter(Token.user_id == id).delete()

    g.session.query(User).filter(User.id == id).delete()
    return {}


@app.route("/users/", methods=['POST'])
@use_sql_session
@authentication_required
def create_user():
    return user2json(
        utils.create_user(
            request.json['username'],
            request.json['password'],
            request.json['first_name'],
            request.json['last_name'],
            request.json.get('is_admin', False),
            g.session
        )
    )