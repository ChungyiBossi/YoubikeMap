from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session
)

def create_sql_engine(url):
    return create_engine(db_url, echo=True)

def create_sql_scoped_session(engine=None):
    if not engine:
        raise Exception("You need to create your db engine first")
    else:
        session_factory = sessionmaker(bind=engine)
        Session = scoped_session(session_factory)
        return Session










