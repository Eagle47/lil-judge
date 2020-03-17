from datetime import timezone

import dateutil.parser
from flask import g, request

from app import app
from decorators import use_sql_session, authentication_required
from orm import Contest, ContestMember
from .constants import ROLES, ROLES_INVERTED


def format_date(d):
    return d.replace(tzinfo=timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")


def contest2json(contest):
    return {
        'id': contest.id,
        'name': contest.name,
        'start_date': format_date(contest.start_date),
        'finish_date': format_date(contest.finish_date),
        'members': [
            {
                'user_id': m.user_id,
                'role': ROLES_INVERTED[m.role]
            } for m in contest.members
        ]
    }


@app.route("/contests/")
@use_sql_session
@authentication_required
def list_contests():
    return {
        'contests': [contest2json(contest) for contest in g.session.query(Contest)]
    }


@app.route("/contests/<id>/")
@use_sql_session
@authentication_required
def get_contest(id):
    return contest2json(
        g.session.query(Contest).filter(Contest.id == id).one()
    )


@app.route("/contests/", methods=['POST'])
@use_sql_session
@authentication_required
def create_contest():
    contest = Contest(
        name=request.json['name'],
        start_date=dateutil.parser.parse(request.json['start_date']),
        finish_date=dateutil.parser.parse(request.json['finish_date'])
    )

    g.session.add(contest)

    g.session.flush()

    return contest2json(contest)


@app.route("/contests/<id>/members/", methods=['PUT'])
@use_sql_session
@authentication_required
def update_contest_members(id):
    for member in request.json.get('add', []):
        g.session.add(ContestMember(
            user_id=member['user_id'],
            contest_id=id,
            role=ROLES[member['role']]
        ))

    for member in request.json.get('remove', []):
        g.session.query(ContestMember).filter(
            ContestMember.contest_id == id and
            ContestMember.user_id == member['user_id'] and
            ContestMember.role == member['role']
        ).delete()

    return contest2json(
        g.session.query(Contest).filter(Contest.id == id).one()
    )
