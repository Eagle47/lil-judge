from dbconfig import get_session
from orm import User

import string
import random
import hashlib


def create_user(username, password, first_name, last_name, is_admin=False, session=None):
    salt = ''.join(random.sample(string.printable, 20))
    hash = hashlib.sha512()
    hash.update((password + salt).encode())
    salted_password = hash.hexdigest()

    s = session or get_session()

    new_user = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=salted_password,
        salt=salt,
        is_admin=is_admin
    )
    s.add(new_user)

    s.flush()

    if session is None:
        s.commit()

    return new_user


def get_user(username, password, session=None):
    s = session or get_session()

    user = s.query(User).filter(User.username == username).one_or_none()

    if user is None:
        return None

    hash = hashlib.sha512()
    hash.update((password + user.salt).encode())

    return user if user.password == hash.hexdigest() else None
