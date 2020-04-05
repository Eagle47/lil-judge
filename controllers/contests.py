from datetime import timezone

import dateutil.parser
from flask import g, request

from app import app
from decorators import use_sql_session, authentication_required
from orm import Contest, ContestMember, Problem, ContestProblem, ProblemTest
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


def problem2json(problem):
    return {
        'id': problem.id,
        'name': problem.name,
        'statement': problem.statement
    }


def contest_problem2json(contest_problem):
    return {
        'contest_id': contest_problem.contest.id,
        'problem_id': contest_problem.problem_id,
        'problem_key': contest_problem.problem_key,
        'problem': [
            {
                'id': contest_problem.problem.id,
                'name': contest_problem.problem.name,
                'statement': contest_problem.problem.statement
            }
        ]
    }


def problem_test2json(problem_test):
    return {
        'id': problem_test.id,
        'problem_id': problem_test.problem_id,
        'input': problem_test.input.decode(),
        'output': problem_test.output.decode()
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


@app.route("/contests/<id>/problems/")
@use_sql_session
@authentication_required
def list_problems(id):
    return {
        'contests_problems': [contest_problem2json(contest_problem) for contest_problem
                              in g.session.query(ContestProblem).filter(ContestProblem.contest_id == id)]
    }


@app.route("/contests/<id>/problems/", methods=['POST'])
@use_sql_session
@authentication_required
def create_problem(id):
    prblm = Problem(
        name=request.json['name'],
        statement=request.json['statement']
    )

    g.session.add(prblm)
    g.session.flush()

    contest_problem = ContestProblem(
        contest_id=id,
        problem_id=prblm.id,
        problem_key=request.json['problem_key']
    )

    g.session.add(contest_problem)
    g.session.flush()

    return contest_problem2json(contest_problem)


@app.route("/contests/<id>/problems/<problem_id>/")
@use_sql_session
@authentication_required
def get_problem(id, problem_id):
    return problem2json(
        g.session.query(ContestProblem).filter((ContestProblem.contest_id == id) & (ContestProblem.problem_id == problem_id)).one().problem
    )


@app.route("/contests/<id>/problems/<problem_id>/tests")
@use_sql_session
@authentication_required
def list_tests(id, problem_id):
    prblm = g.session.query(ContestProblem).filter((ContestProblem.contest_id == id) & (ContestProblem.problem_id == problem_id)).one().problem
    return {
        'tests': [problem_test2json(problem_test) for problem_test in prblm.tests]
    }


@app.route("/contests/<id>/problems/<problem_id>/tests/", methods=['POST'])
@use_sql_session
@authentication_required
def create_test(id, problem_id):
    problem_test = ProblemTest(
        problem_id=problem_id,
        input=request.json['input'].encode(),
        output=request.json['output'].encode()
    )

    g.session.add(problem_test)
    g.session.flush()

    return problem_test2json(problem_test)


@app.route("/contests/<id>/problems/<problem_id>/tests/<test_id>/")
@use_sql_session
@authentication_required
def get_test(id, problem_id, test_id):
    return problem_test2json(
        g.session.query(ProblemTest).filter(ProblemTest.id == test_id).one()
    )
