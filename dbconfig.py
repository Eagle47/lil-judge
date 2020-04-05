from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

config = {
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': 5432,
    'echo': True
}


def get_engine():
    return create_engine(
        'postgresql://{user}:{password}@{host}:{port}'.format(**config),
        echo=config['echo']
    )


def get_session():
    return sessionmaker(bind=get_engine())()
