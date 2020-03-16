from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Boolean, Integer, String, UniqueConstraint, ForeignKey, DateTime
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
