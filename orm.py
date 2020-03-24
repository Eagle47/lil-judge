from sqlalchemy import Column, Boolean, Integer, String, UniqueConstraint, ForeignKey, DateTime, LargeBinary, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    salt = Column(String)
    is_admin = Column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint('username'),
    )


class Contest(Base):
    __tablename__ = 'contests'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    start_date = Column(DateTime(timezone=True))
    finish_date = Column(DateTime(timezone=True))
    paused = Column(Boolean, default=False)

    members = relationship('ContestMember')
    problems = relationship('ContestProblem')
    submissions = relationship('ProblemSubmission')


class Problem(Base):
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    statement = Column(String)

    tests = relationship('ProblemTest')


class ContestProblem(Base):
    __tablename__ = 'contests_problems'

    contest_id = Column(Integer, ForeignKey('contests.id'), primary_key=True)
    problem_id = Column(Integer, ForeignKey('problems.id'), primary_key=True)
    problem_key = Column(String, primary_key=True)

    contest = relationship('Contest')
    problem = relationship('Problem')

    #submissions = relationship('ProblemSubmission', foreign_keys=[contest_id, problem_id])

    __table_args__ = (
        UniqueConstraint('contest_id', 'problem_key'),
    )


class ProblemTest(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True)
    problem_id = Column(Integer, ForeignKey('problems.id'))
    input = Column(LargeBinary)
    output = Column(LargeBinary)


class ProblemSubmission(Base):
    __tablename__ = 'problems_submissions'

    id = Column(Integer, primary_key=True)
    contest_id = Column(Integer, ForeignKey('contests.id'))
    problem_id = Column(Integer, ForeignKey('problems.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    results = Column(JSON, nullable=True)

    submitted_at = Column(DateTime(timezone=True))

    source = Column(LargeBinary)


class ContestMember(Base):
    __tablename__ = 'contest_membership'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    contest_id = Column(Integer, ForeignKey('contests.id'), primary_key=True)
    role = Column(Integer, primary_key=True)

    user = relationship("User")
    contest = relationship("Contest")


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User")
