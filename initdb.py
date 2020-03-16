from dbconfig import get_engine
from orm import Base
from controllers.utils import create_user

engine = get_engine()

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

create_user('test', 'test', 'John', 'Doe')
